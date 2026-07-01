"""Controller layer package for UI-to-service orchestration."""

from repositories.course_repository import CourseRepository
from repositories.lesson_repository import LessonRepository
from repositories.measurement_repository import MeasurementRepository
from repositories.schedule_repository import ScheduleRepository
from repositories.student_repository import StudentRepository
from services.course_service import CourseService
from services.lesson_service import LessonService
from services.measurement_service import MeasurementService
from services.schedule_service import ScheduleService
from services.student_service import StudentService

from .course_controller import CourseController
from .lesson_controller import LessonController
from .measurement_controller import MeasurementController
from .schedule_controller import ScheduleController
from .student_controller import StudentController


def build_student_controller() -> StudentController:
	student_repository = StudentRepository()
	student_service = StudentService(student_repository=student_repository)
	return StudentController(student_service=student_service)


def build_course_controller() -> CourseController:
	course_repository = CourseRepository()
	student_repository = StudentRepository()
	course_service = CourseService(
		course_repository=course_repository,
		student_repository=student_repository,
	)
	return CourseController(course_service=course_service)


def build_schedule_controller() -> ScheduleController:
	schedule_repository = ScheduleRepository()
	schedule_service = ScheduleService(schedule_repository=schedule_repository)
	return ScheduleController(schedule_service=schedule_service)


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


def build_measurement_controller() -> MeasurementController:
	measurement_repository = MeasurementRepository()
	measurement_service = MeasurementService(measurement_repository=measurement_repository)
	return MeasurementController(measurement_service=measurement_service)


__all__ = [
	"StudentController",
	"CourseController",
	"ScheduleController",
	"LessonController",
	"MeasurementController",
	"build_student_controller",
	"build_course_controller",
	"build_schedule_controller",
	"build_lesson_controller",
	"build_measurement_controller",
]
