"""Controller layer package for UI-to-service orchestration."""

from repositories.course_repository import CourseRepository
from repositories.lesson_repository import LessonRepository
from repositories.student_repository import StudentRepository
from services.lesson_service import LessonService

from .lesson_controller import LessonController
from .student_controller import StudentController


def build_lesson_controller() -> LessonController:
	lesson_repository = LessonRepository()
	student_repository = StudentRepository()
	course_repository = CourseRepository()
	lesson_service = LessonService(
		lesson_repository=lesson_repository,
		student_repository=student_repository,
		course_repository=course_repository,
	)
	return LessonController(lesson_service=lesson_service)

__all__ = ["StudentController", "LessonController", "build_lesson_controller"]
