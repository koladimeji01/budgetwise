import logging


# ==========================================
# LOGGER CONFIGURATION
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# ==========================================
# APPLICATION LOGGER
# ==========================================

logger = logging.getLogger("budgetwise")
