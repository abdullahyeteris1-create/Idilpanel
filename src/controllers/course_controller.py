"""Course controller skeleton for UI-to-service request orchestration."""

from __future__ import annotations

from services.course_service import CourseService


class CourseController:
    """Bridge UI requests to CourseService without business logic."""

    def __init__(self, course_service: CourseService) -> None:
        self._course_service = course_service

    def create_course(self, data):
        return self._course_service.create_course(data)

    def get_course(self, record_id):
        return self._course_service.get_course(record_id)

    def list_courses(self, limit: int = 100, offset: int = 0):
        return self._course_service.list_courses(limit, offset)

    def update_course(self, record_id, data):
        return self._course_service.update_course(record_id, data)

    def delete_course(self, record_id):
        return self._course_service.delete_course(record_id)

    def assign_course_to_student(self, student_id: int, kur_no: int):
        """Assign a course to a student (business operation)."""
        return self._course_service.assign_course_to_student(student_id, kur_no)

    def get_students_for_course(self, course_id: int):
        """Get all students assigned to a specific course."""
        return self._course_service.get_students_for_course(course_id)

    def get_students_by_kur(self, kur_no: int):
        """Get all students assigned to a specific course level (kur)."""
        return self._course_service.get_students_by_kur(kur_no)

    def count_students_for_kur(self, kur_no: int):
        """Get the number of active students in a kur level."""
        return self._course_service.count_students_for_kur(kur_no)

    def get_occupancy_rate_for_kur(self, kur_no: int):
        """Get the occupancy rate (%) for a kur level."""
        return self._course_service.get_occupancy_rate_for_kur(kur_no)

    def get_effective_status_for_kur(self, kur_no: int):
        """Get the effective display status for a kur level."""
        return self._course_service.get_effective_status_for_kur(kur_no)

    def get_course_capacity_info(self, kur_no: int):
        """Get complete capacity information for a kur level."""
        max_capacity = self._course_service._MAX_CAPACITY_PER_KUR
        current_count = self.count_students_for_kur(kur_no)
        occupancy_rate = self.get_occupancy_rate_for_kur(kur_no)
        status = self.get_effective_status_for_kur(kur_no)
        
        return {
            "kur_no": kur_no,
            "max_capacity": max_capacity,
            "current_count": current_count,
            "occupancy_rate": occupancy_rate,
            "status": status,
        }

    def can_assign_student_to_kur(self, student_id: int, kur_no: int):
        """Validate whether a student can be assigned to a kur level."""
        can_assign, reason = self._course_service.can_assign_student_to_kur(student_id, kur_no)
        return can_assign, reason
