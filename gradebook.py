# gradebook.py -- the department gradebook service
import json
import logging
import sys
import http.server
from typing import Any, Dict, Tuple, List

from errors import ConflictError, GradebookError, NotFoundError, ValidationError
from models import parse_assessment, parse_mark, parse_student

DATA = "gradebook.json"
STATE: Dict[str, Any] = {"students": {}, "assessments": {}, "marks": []}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load() -> None:
    """Load gradebook state from JSON file."""
    global STATE
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            STATE = json.load(f)
    except FileNotFoundError:
        STATE = {"students": {}, "assessments": {}, "marks": []}


def save() -> None:
    """Save gradebook state to JSON file."""
    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(STATE, f, indent=2)


def get_students() -> List[Dict[str, Any]]:
    """Return list of all students."""
    return list(STATE["students"].values())


def get_student(sid: str) -> Dict[str, Any]:
    """Return a single student by ID."""
    if sid not in STATE["students"]:
        raise NotFoundError(f"Student '{sid}' not found.")
    
    st = STATE["students"][sid].copy()
    student_marks = [m for m in STATE["marks"] if m["student"] == sid]
    
    if not student_marks:
        st["percentage"] = "0"
        return st

    total_earned = 0.0
    total_possible = 0.0
    for m in student_marks:
        aid = m["assessment"]
        if aid in STATE["assessments"]:
            total_earned += float(m["score"])
            total_possible += float(STATE["assessments"][aid]["total"])

    if total_possible > 0:
        pct = (total_earned / total_possible) * 100
        st["percentage"] = str(round(pct, 2))
    else:
        st["percentage"] = "0"

    return st


def get_assessments() -> List[Dict[str, Any]]:
    """Return list of all assessments."""
    return list(STATE["assessments"].values())


def get_report() -> List[Dict[str, Any]]:
    """Generate summary report for all students."""
    res = []
    for sid in STATE["students"]:
        st = get_student(sid)
        res.append({"id": st["id"], "name": st["name"], "pct": st.get("percentage", "0")})
    return res


def add_student(payload: Any) -> Dict[str, Any]:
    """Add a new student."""
    st = parse_student(payload)
    if st.id in STATE["students"]:
        raise ConflictError(f"Student with id '{st.id}' already exists.")

    data = {"id": st.id, "name": st.name}
    STATE["students"][st.id] = data
    save()
    return data


def add_assessment(payload: Any) -> Dict[str, Any]:
    """Add a new assessment."""
    asm = parse_assessment(payload)
    if asm.id in STATE["assessments"]:
        raise ConflictError(f"Assessment with id '{asm.id}' already exists.")

    data = {
        "id": asm.id,
        "title": asm.title,
        "weight": asm.weight,
        "total": asm.total,
    }
    STATE["assessments"][asm.id] = data
    save()
    return data


def add_mark(payload: Any) -> Dict[str, Any]:
    """Add a mark for an assessment."""
    m = parse_mark(payload)
    if m.student not in STATE["students"]:
        raise NotFoundError(f"Student '{m.student}' does not exist.")
    if m.assessment not in STATE["assessments"]:
        raise NotFoundError(f"Assessment '{m.assessment}' does not exist.")

    asm = STATE["assessments"][m.assessment]
    if m.score > asm["total"]:
        raise ValidationError(f"Score {m.score} exceeds maximum total of {asm['total']}.")

    mark_data = {
        "student": m.student,
        "assessment": m.assessment,
        "score": m.score,
    }
    STATE["marks"].append(mark_data)
    save()
    return {"ok": True}


class Handler(http.server.BaseHTTPRequestHandler):
    """HTTP Request handler with centralized error boundary."""

    def _send(self, code: int, body: Any) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def _parse_json_body(self) -> Any:
        length_header = self.headers.get("Content-Length")
        if not length_header:
            raise ValidationError("Missing Content-Length header.")
        try:
            length = int(length_header)
        except ValueError:
            raise ValidationError("Invalid Content-Length header.") from None

        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except Exception:
            raise ValidationError("Invalid JSON payload.") from None

    def _handle_request(self, method: str) -> Tuple[int, Any]:
        path = self.path.strip("/")
        parts = path.split("/") if path else []

        if method == "GET":
            if not parts:
                return 200, {"status": "ok"}
            if parts[0] == "students":
                if len(parts) == 1:
                    return 200, get_students()
                if len(parts) == 2:
                    return 200, get_student(parts[1])
            elif parts[0] == "assessments" and len(parts) == 1:
                return 200, get_assessments()
            elif parts[0] == "report" and len(parts) == 1:
                return 200, get_report()
            raise NotFoundError("Route not found.")

        elif method == "POST":
            payload = self._parse_json_body()
            if not parts:
                raise NotFoundError("Route not found.")
            if parts[0] == "students" and len(parts) == 1:
                return 200, add_student(payload)
            if parts[0] == "assessments" and len(parts) == 1:
                return 200, add_assessment(payload)
            if parts[0] == "marks" and len(parts) == 1:
                return 200, add_mark(payload)
            raise NotFoundError("Route not found.")

        raise NotFoundError("Method not supported.")

    def _dispatch(self, method: str) -> None:
        try:
            status, body = self._handle_request(method)
            self._send(status, body)
        except ValidationError as e:
            self._send(400, {"error": str(e)})
        except NotFoundError as e:
            self._send(404, {"error": str(e)})
        except ConflictError as e:
            self._send(409, {"error": str(e)})
        except GradebookError as e:
            self._send(400, {"error": str(e)})
        except Exception:
            logging.exception("Unhandled server error")
            self._send(500, {"error": "internal error"})

    def do_GET(self) -> None:
        self._dispatch("GET")

    def do_POST(self) -> None:
        self._dispatch("POST")


def main() -> None:
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    load()
    logging.info("gradebook on %d", port)
    server = http.server.HTTPServer(("", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()