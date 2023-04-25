OLD_DOMAIN = "www.essex.gov.uk"
OLD_BASE_URL = f"https://{OLD_DOMAIN}"

MIGRATION_TEST_DOMAIN = "beta.essex.gov.uk"
MIGRATION_TEST_BASE_URL = f"https://{MIGRATION_TEST_DOMAIN}"
MIGRATION_TEST_START_URL = MIGRATION_TEST_BASE_URL + \
    "/births-ceremonies-and-deaths/get-married-or-form-civil-partnership"

CONTENTFUL_DOMAIN = "assets.ctfassets.net"
CONTENTFUL_BASE_URL = f"https://{CONTENTFUL_DOMAIN}"

# First, include everything as a non-prod domain
ALL_DOMAINS = [
    # Main prod domains for existing site
    "www.essex.gov.uk",
    "essex.gov.uk",
    "preview.essex.gov.uk",

    # Old migration test environment
    "portal.whitemoss-5a7067b3.uksouth.azurecontainerapps.io",

    # Dev environment
    "essex-gov.nomensa.xyz",
    "dev.essex-gov.nomensa.xyz",

    # Pre-production environment
    "portal.nicedesert-14326f17.uksouth.azurecontainerapps.io",
    "essex-gov-pp.nomensa.xyz",
    "preprod.essex-gov.nomensa.xyz",

    # Production environment
    "portal.icydesert-8c4242e9.uksouth.azurecontainerapps.io",
    "www-essex-gov-uk.nomensa.xyz",
    "beta.essex-gov.nomensa.xyz",
    "beta.essex.gov.uk",
]

NON_PROD_DOMAINS = ALL_DOMAINS

# Remove the migration test domain from here, just leaving the others
NON_PROD_DOMAINS.remove(MIGRATION_TEST_DOMAIN)
NON_PROD_DOMAINS = frozenset(NON_PROD_DOMAINS)
