# Standard library imports
from logging import getLogger

# Local application imports
from src.config import server
import sys

logger = getLogger(__name__)

n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")

PORT=int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8000
def main() -> None:
    print(PORT)
    server.run(PORT)
   


if __name__ == "__main__":

    try:
        main()
    except BaseException as error:
        logger.error(f"Unexpected {error=}, {type(error)=}")
