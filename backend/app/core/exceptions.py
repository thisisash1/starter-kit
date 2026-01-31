class AppException(Exception):
  """애플리케이션 기본 예외"""

  def __init__(self, message: str, status_code: int = 400):
    self.message = message
    self.status_code = status_code
    super().__init__(self.message)


class NotFoundException(AppException):
  """리소스 없음 예외"""

  def __init__(self, message: str = "리소스를 찾을 수 없습니다"):
    super().__init__(message, status_code=404)


class ValidationException(AppException):
  """유효성 검증 실패 예외"""

  def __init__(self, message: str = "입력값이 유효하지 않습니다"):
    super().__init__(message, status_code=422)


class DuplicateException(AppException):
  """중복 데이터 예외"""

  def __init__(self, message: str = "이미 존재하는 데이터입니다"):
    super().__init__(message, status_code=409)
