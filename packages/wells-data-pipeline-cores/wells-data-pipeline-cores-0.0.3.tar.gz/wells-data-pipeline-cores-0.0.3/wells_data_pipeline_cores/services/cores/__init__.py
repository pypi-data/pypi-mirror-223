from __future__ import absolute_import

import logging

# import base services into services package
try:
    from wells_data_pipeline_cores.services.cores.az_ad_authz_service import AzAuthzService
except Exception as ex:
    logging.warning("Export AzAuthzService error - %s", ex)

try:
    from wells_data_pipeline_cores.services.cores.send_email_service import SendEmailService
except Exception as ex:
    logging.warning("Export SendEmailService error - %s", ex)

# support Snowflake
try:
    from wells_data_pipeline_cores.services.cores.snow_data_service import SnowDataService
except Exception as ex:
    logging.warning("Export SnowDataService error - %s", ex)

# support Az Storage Account
try:
    from wells_data_pipeline_cores.services.cores.az_storage_account_service import AzStorageAccountService
except Exception as ex:
    logging.warning("Export AzStorageAccountService error - %s", ex)

# support Az Cosmos DB
try:
    from wells_data_pipeline_cores.services.cores.az_cosmos_data_service import AzCosmosDataService, AzCosmosPartitionKeyModel
except Exception as ex:
    logging.warning("Export AzCosmosDataService error - %s", ex)

# support Az ADX
try:
    from wells_data_pipeline_cores.services.cores.az_adx_data_service import  AzAdxDataService 
except Exception as ex:
    logging.warning("Export AzAdxDataService error - %s", ex)

# support WellsETLService
try:
    from wells_data_pipeline_cores.services.cores.wells_etl_service import WellsETLService
except Exception as ex:
    logging.warning("Export WellsETLService error - %s", ex)