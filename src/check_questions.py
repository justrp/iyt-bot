import os
import sys
import traceback

from utils import questionnaire



class QuestionsCheckError(Exception):
    """Base class for custom exceptions"""

    pass


class BothQuestionAndImageError(QuestionsCheckError):
    """Raised when both `question` and `image` fields are presented in the file"""

    pass


class CorrectOptionsMissmatchError(QuestionsCheckError):
    """Raised when there are less than 2 options in the file"""

    pass


class NotEnoughOptionsError(QuestionsCheckError):
    """Raised when there are less than 2 options in the file"""

    pass


class ImageNotFoundError(QuestionsCheckError):
    """Raised when mentioned image was not found in imgs directory"""

    pass


class NoQuestionError(QuestionsCheckError):
    """Raised when no `question` or `image` field is presented in the file"""

    pass


if __name__ == "__main__":
    errors = []
    for q in questionnaire._list_questions():
        try:
            data = questionnaire._get_question(q)
            if "image" in data:
                if "question" in data:
                    raise BothQuestionAndImageError()
                if not os.path.exists(data["image"]):
                    raise ImageNotFoundError()
            elif "question" not in data:
                raise NoQuestionError()
            if len(data["options"]) < 2:
                raise NotEnoughOptionsError()
            if data["correct"] not in data["options"]:
                raise CorrectOptionsMissmatchError()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errors.append((q, f"Could not parse - {exc_type} - {traceback.extract_tb(exc_traceback)}"))

    if len(errors) == 0:
        print("Tests succeeded")
    else:
        for f, err in errors:
            print(f"{f} - {err}")
        exit(1)
