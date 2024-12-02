# from rasa_nlu_examples.common import NotInstalled
#
# # Thử nhập khẩu UndertheseaTokenizer, nếu không tìm thấy thì sẽ thông báo lỗi và không tải
try:
    from components.tokenizer import UndertheseaTokenizer
except ImportError:
    UndertheseaTokenizer = NotInstalled("UndertheseaTokenizer", "underthesea")

__all__ = ["UndertheseaTokenizer"]
