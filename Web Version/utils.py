import bcrypt
import random
from datetime import datetime

def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(hashed_password: bytes, password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode(), hashed_password)

def generate_typing_text() -> str:
    """Generate a random typing text."""
    texts = [
        "The future of technology lies in artificial intelligence and machine learning. As computers become more powerful, they can process vast amounts of data and solve complex problems. Scientists and engineers work together to create smart systems that can understand human language, recognize patterns, and make decisions. These advances are changing the way we live and work, making our daily tasks easier and more efficient.",
        "In the digital age, coding has become an essential skill. Whether you're building websites, developing mobile apps, or analyzing data, programming knowledge opens up endless possibilities. From Python to JavaScript, the tools of modern software development are powerful and accessible to anyone willing to learn.",
        "The world is becoming increasingly connected. Smart devices, the Internet of Things, and cloud computing are transforming how we live and work. As technology advances, it's important to stay informed about the latest trends and developments in the tech industry."
    ]
    return random.choice(texts)

def calculate_typing_speed(words_typed: int, time_elapsed: float) -> float:
    """Calculate typing speed in words per minute."""
    return (words_typed / time_elapsed) * 60

def calculate_accuracy(correct_chars: int, total_chars: int) -> float:
    """Calculate typing accuracy as a percentage."""
    return (correct_chars / total_chars) * 100 if total_chars > 0 else 0
