from utils.elapsed import timeit
from utils.logger import get_logger
from utils.pd import deduplicated

logger = get_logger(__name__)


@timeit
def main():
    result = deduplicated("./tests/test_0.csv", ["draw"], "last")
    logger.info(result)


if __name__ == "__main__":
    main()
