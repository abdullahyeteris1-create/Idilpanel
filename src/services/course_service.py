"""Course service skeleton for course domain operations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from repositories.course_repository import CourseRepository
from repositories.student_repository import StudentRepository

from .base_service import BaseService


class CourseService(BaseService):
    """Service entry point for course-related operations."""

    _NAME_FIELDS = ("course_name", "name", "kurs_adi")
    _ACTIVE_FIELDS = ("is_active", "active", "durum", "status")
    _LEVEL_FIELDS = ("course_level", "level", "kur_no", "kur")
    _DURATION_FIELDS = ("duration", "duration_weeks", "sure", "total_lessons")

    _LEVEL_MIN = 1
    _LEVEL_MAX = 12
    _MAX_CAPACITY_PER_KUR = 30  # Maximum students per course level

    def __init__(
        self,
        course_repository: CourseRepository | None = None,
        student_repository: StudentRepository | None = None,
        repositories: dict[str, Any] | None = None,
    ) -> None:
        merged_repositories = dict(repositories or {})
        if course_repository is not None:
            merged_repositories["course"] = course_repository
        if student_repository is not None:
            merged_repositories["student"] = student_repository
        super().__init__(merged_repositories)

    # CRUD Operations
    def create_course(self, data):
        validated_data = self.validate_course(data)
        repository_payload = self._to_repository_payload(validated_data)
        return self.get_repository("course").create(repository_payload)

    def get_course(self, record_id):
        return self.get_repository("course").get_by_id(record_id)

    def list_courses(self, limit: int = 100, offset: int = 0):
        return self.get_repository("course").list_all(limit, offset)

    def update_course(self, record_id, data):
        validated_data = self.validate_course(data, current_course_id=record_id)
        repository_payload = self._to_repository_payload(validated_data)
        return self.get_repository("course").update(record_id, repository_payload)

    def delete_course(self, record_id):
        return self.get_repository("course").delete(record_id)

    # Business Operations
    def assign_course_to_student(self, student_id: int, kur_no: int) -> dict[str, Any]:
        """
        Assign a course to a student.
        Enforces the business rules:
        - Student can only have one active course at a time
        - Student can only be assigned to Aktif (active) courses
        - Course must have capacity available (not at max capacity)
        - Student cannot be re-assigned to the same active course
        
        Args:
            student_id: The student ID to assign the course to
            kur_no: The course level (1-12)
            
        Returns:
            The created course record
            
        Raises:
            ValueError: If validation fails
        """
        if not student_id or student_id <= 0:
            raise ValueError("Student ID must be a positive integer")
        
        if not kur_no or kur_no < self._LEVEL_MIN or kur_no > self._LEVEL_MAX:
            raise ValueError(f"Course level must be between {self._LEVEL_MIN} and {self._LEVEL_MAX}")
        
        # Validate assignment is allowed
        can_assign, reason = self.can_assign_student_to_kur(student_id, kur_no)
        if not can_assign:
            raise ValueError(reason)
        
        repository = self.get_repository("course")
        
        # Check if student already has an active course
        all_courses = repository.list_all(limit=1000, offset=0)
        active_course_for_student = None
        
        for course in all_courses:
            if not isinstance(course, Mapping):
                continue
            
            course_student_id = course.get("student_id")
            course_durum = str(course.get("durum", "")).strip()
            course_is_active = course.get("is_active", 1)
            
            if int(course_student_id or 0) == int(student_id) and course_durum == "Aktif" and int(course_is_active or 0) == 1:
                active_course_for_student = course
                break
        
        # If student has an active course, deactivate it
        if active_course_for_student:
            active_course_id = active_course_for_student.get("id")
            if active_course_id:
                repository.update(active_course_id, {"durum": "Beklemede"})
        
        # Create new active course
        from datetime import date as date_class
        
        payload = {
            "student_id": student_id,
            "kur_no": kur_no,
            "baslangic": date_class.today().isoformat(),
            "durum": "Aktif",
            "hedef_ders_sayisi": 16,
            "is_active": 1,
        }
        
        course_id = repository.create(payload)
        
        # Fetch and return the created course
        return repository.get_by_id(course_id)

    def get_students_for_course(self, course_id: int) -> list[dict[str, Any]]:
        """
        Get all students assigned to a specific course.
        
        Args:
            course_id: The course ID
            
        Returns:
            List of student records assigned to the course
        """
        if not course_id or course_id <= 0:
            return []
        
        course_repo = self.get_repository("course")
        student_repo = self.get_repository("student")
        
        if student_repo is None:
            return []
        
        # Get the course record
        course = course_repo.get_by_id(course_id)
        if course is None:
            return []
        
        student_id = course.get("student_id")
        if not student_id:
            return []
        
        # Get student details
        student = student_repo.get_by_id(student_id)
        if student is None:
            return []
        
        # Return list with single student (courses table has one student per row)
        return [student]

    def get_students_by_kur(self, kur_no: int) -> list[dict[str, Any]]:
        """
        Get all students assigned to a specific course level (kur).
        
        Args:
            kur_no: The course level (1-12)
            
        Returns:
            List of student records assigned to this kur level
        """
        if not kur_no or kur_no < self._LEVEL_MIN or kur_no > self._LEVEL_MAX:
            return []
        
        course_repo = self.get_repository("course")
        student_repo = self.get_repository("student")
        
        if student_repo is None:
            return []
        
        # Get all courses with this kur level
        all_courses = course_repo.list_all(limit=1000, offset=0)
        student_ids = set()
        
        for course in all_courses:
            if not isinstance(course, Mapping):
                continue
            
            course_kur = course.get("kur_no")
            course_is_active = course.get("is_active", 1)
            
            if int(course_kur or 0) == int(kur_no) and int(course_is_active or 0) == 1:
                student_id = course.get("student_id")
                if student_id:
                    student_ids.add(student_id)
        
        # Fetch student details for each student ID
        students = []
        for student_id in student_ids:
            student = student_repo.get_by_id(student_id)
            if student is not None:
                students.append(student)
        
        return students

    def count_students_for_kur(self, kur_no: int) -> int:
        """
        Count the number of active students assigned to a specific kur level.
        
        Args:
            kur_no: The course level (1-12)
            
        Returns:
            Number of active students in this kur level
        """
        if not kur_no or kur_no < self._LEVEL_MIN or kur_no > self._LEVEL_MAX:
            return 0
        
        course_repo = self.get_repository("course")
        all_courses = course_repo.list_all(limit=1000, offset=0)
        
        count = 0
        for course in all_courses:
            if not isinstance(course, Mapping):
                continue
            
            course_kur = course.get("kur_no")
            course_durum = str(course.get("durum", "")).strip()
            course_is_active = course.get("is_active", 1)
            
            # Count only active courses (durum='Aktif') with is_active=1
            if (int(course_kur or 0) == int(kur_no) and 
                course_durum == "Aktif" and 
                int(course_is_active or 0) == 1):
                count += 1
        
        return count

    def get_occupancy_rate_for_kur(self, kur_no: int) -> float:
        """
        Calculate the occupancy rate (as percentage) for a kur level.
        
        Args:
            kur_no: The course level (1-12)
            
        Returns:
            Occupancy rate as percentage (0-100)
        """
        if not kur_no or kur_no < self._LEVEL_MIN or kur_no > self._LEVEL_MAX:
            return 0.0
        
        current_count = self.count_students_for_kur(kur_no)
        max_capacity = self._MAX_CAPACITY_PER_KUR
        
        if max_capacity <= 0:
            return 0.0
        
        return round((current_count / max_capacity) * 100, 2)

    def get_effective_status_for_kur(self, kur_no: int) -> str:
        """
        Get the effective display status for a kur level.
        
        Computed based on:
        - If any course is Tamamlandi/Iptal → "Tamamlandı"
        - If at max capacity → "Kontenjan Dolu"
        - If any course is Aktif → "Aktif"
        - If all courses are Beklemede → "Pasif"
        - If no courses exist → "Aktif" (allow setting up first course)
        
        Args:
            kur_no: The course level (1-12)
            
        Returns:
            Effective status: "Aktif", "Pasif", "Kontenjan Dolu", "Tamamlandı"
        """
        if not kur_no or kur_no < self._LEVEL_MIN or kur_no > self._LEVEL_MAX:
            return "Pasif"
        
        course_repo = self.get_repository("course")
        all_courses = course_repo.list_all(limit=1000, offset=0)
        
        has_completed = False
        has_active = False
        has_pending = False
        has_any = False
        
        for course in all_courses:
            if not isinstance(course, Mapping):
                continue
            
            course_kur = course.get("kur_no")
            course_durum = str(course.get("durum", "")).strip()
            course_is_active = course.get("is_active", 1)
            
            if int(course_kur or 0) == int(kur_no) and int(course_is_active or 0) == 1:
                has_any = True
                if course_durum in ("Tamamlandi", "Iptal"):
                    has_completed = True
                elif course_durum == "Aktif":
                    has_active = True
                elif course_durum == "Beklemede":
                    has_pending = True
        
        # Priority order
        if has_completed:
            return "Tamamlandı"
        
        current_count = self.count_students_for_kur(kur_no)
        if current_count >= self._MAX_CAPACITY_PER_KUR:
            return "Kontenjan Dolu"
        
        if has_active:
            return "Aktif"
        
        if has_pending:
            return "Pasif"
        
        # No courses for this kur yet - allow setting up first course
        if not has_any:
            return "Aktif"
        
        return "Pasif"

    def can_assign_student_to_kur(self, student_id: int, kur_no: int) -> tuple[bool, str]:
        """
        Validate whether a student can be assigned to a kur level.
        
        Business rules:
        - Student can only be assigned to Aktif courses
        - Course must have capacity available
        - Student cannot be re-assigned to the same active course
        
        Args:
            student_id: The student ID
            kur_no: The course level (1-12)
            
        Returns:
            Tuple of (can_assign: bool, reason: str)
            Reason is error message if cannot assign, empty string if can assign
        """
        if not student_id or student_id <= 0:
            return False, "Geçersiz öğrenci ID."
        
        if not kur_no or kur_no < self._LEVEL_MIN or kur_no > self._LEVEL_MAX:
            return False, f"Kur seviyesi {self._LEVEL_MIN} ile {self._LEVEL_MAX} arasında olmalıdır."
        
        course_repo = self.get_repository("course")
        
        # Check if student is already assigned to this kur level with active status
        all_courses = course_repo.list_all(limit=1000, offset=0)
        for course in all_courses:
            if not isinstance(course, Mapping):
                continue
            
            course_student_id = course.get("student_id")
            course_kur = course.get("kur_no")
            course_durum = str(course.get("durum", "")).strip()
            course_is_active = course.get("is_active", 1)
            
            if (int(course_student_id or 0) == int(student_id) and
                int(course_kur or 0) == int(kur_no) and
                course_durum == "Aktif" and
                int(course_is_active or 0) == 1):
                return False, "Bu kursa zaten atanmışsınız."
        
        # Check if kur is passive
        effective_status = self.get_effective_status_for_kur(kur_no)
        if effective_status == "Pasif":
            return False, "Pasif kurslara öğrenci atanamaz."
        
        if effective_status == "Tamamlandı":
            return False, "Tamamlanan kurslara öğrenci atanamaz."
        
        # Check if kur is at capacity
        if effective_status == "Kontenjan Dolu":
            return False, "Bu kursun kontenjanı dolmuştur."
        
        return True, ""

    # Validation
    def validate_course(self, data: Any | None = None, current_course_id: int | None = None):
        if data is None:
            return None

        if not isinstance(data, Mapping):
            raise ValueError("course data must be a mapping")

        repository = self.get_repository("course")

        course_name = self._get_field_value(data, self._NAME_FIELDS)
        if course_name is None or not course_name:
            raise ValueError("course name cannot be empty")

        if hasattr(repository, "list_all"):
            self._ensure_unique_active_name(repository, course_name, current_course_id)

        level_value = self._get_field_value(data, self._LEVEL_FIELDS)
        if level_value is not None and level_value:
            level = self._parse_int(level_value, "course level")
            if level < self._LEVEL_MIN or level > self._LEVEL_MAX:
                raise ValueError(
                    f"course level must be between {self._LEVEL_MIN} and {self._LEVEL_MAX}"
                )

        duration_value = self._get_field_value(data, self._DURATION_FIELDS)
        if duration_value is not None and duration_value:
            duration = self._parse_float(duration_value, "course duration")
            if duration <= 0:
                raise ValueError("course duration must be a positive value")

        return data

    def _get_field_value(self, data: Mapping[str, Any], field_names: tuple[str, ...]) -> str | None:
        for field_name in field_names:
            if field_name in data:
                value = data[field_name]
                if value is None:
                    return ""
                return str(value).strip()
        return None

    def _ensure_unique_active_name(
        self,
        repository: CourseRepository,
        course_name: str,
        current_course_id: int | None = None,
    ) -> None:
        existing_courses = repository.list_all(limit=1000, offset=0)
        for existing_course in existing_courses:
            if not isinstance(existing_course, Mapping):
                continue

            existing_name = self._get_field_value(existing_course, self._NAME_FIELDS)
            if existing_name is None:
                continue

            if existing_name.casefold() != course_name.casefold():
                continue

            existing_id = existing_course.get("id")
            if current_course_id is not None and existing_id == current_course_id:
                continue

            if self._is_active(existing_course):
                raise ValueError("an active course with the same name already exists")

    def _is_active(self, data: Mapping[str, Any]) -> bool:
        for field_name in self._ACTIVE_FIELDS:
            if field_name not in data:
                continue

            value = data[field_name]
            if isinstance(value, bool):
                return value

            text = str(value).strip().casefold()
            return text in {"1", "true", "aktif", "active", "yes"}

        return True

    def _parse_int(self, value: str, field_label: str) -> int:
        try:
            return int(value)
        except ValueError as exc:
            raise ValueError(f"{field_label} must be a valid integer") from exc

    def _parse_float(self, value: str, field_label: str) -> float:
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"{field_label} must be a valid number") from exc

    def _to_repository_payload(self, data: Mapping[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {}

        if "student_id" in data:
            payload["student_id"] = data["student_id"]

        level_value = self._get_field_value(data, self._LEVEL_FIELDS)
        if level_value is not None and level_value:
            payload["kur_no"] = self._parse_int(level_value, "course level")

        start_date = data.get("baslangic")
        if start_date is not None:
            payload["baslangic"] = str(start_date).strip()

        end_date = data.get("bitis")
        if end_date is not None:
            cleaned_end_date = str(end_date).strip()
            if cleaned_end_date:
                payload["bitis"] = cleaned_end_date

        status_value = data.get("durum")
        if status_value is not None:
            payload["durum"] = str(status_value).strip()

        duration_value = self._get_field_value(data, self._DURATION_FIELDS)
        if duration_value is not None and duration_value:
            payload["hedef_ders_sayisi"] = self._parse_int(duration_value, "course duration")

        if "is_active" in data:
            payload["is_active"] = data["is_active"]

        return payload
