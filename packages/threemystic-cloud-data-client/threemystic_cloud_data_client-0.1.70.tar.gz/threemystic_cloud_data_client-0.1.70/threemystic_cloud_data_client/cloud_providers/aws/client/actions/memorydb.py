"""The AWS database Action. This will pull the AWS rds"""
from threemystic_cloud_data_client.cloud_providers.aws.client.actions.base_class.base import cloud_data_client_aws_client_action_base as base
import asyncio

#add elasticache
class cloud_data_client_aws_client_action(base):
  def __init__(self, *args, **kwargs):
    super().__init__(
      data_action="memorydb",
      logger_name= "cloud_data_client_aws_client_action_memorydb",
      *args, **kwargs)
    
    
    self.data_id_name = "Name"
    
    self.arn_lambda = (lambda item: self.get_cloud_client().get_resource_general_arn(
      resource_type= "memorydb",
      resource_type_sub= "cluster", **item # {region, account_id, resource_id}
    ))
    
    self.auto_region_resourcebytype= ["Amazon MemoryDB"]
    self.resource_group_filter = [
    {
      'Name': 'resource-type',
      'Values': [
        'AWS::MemoryDB::Cluster',
      ]
    }
  ]
    
  
  async def __get_memorydb_tags(self, client, account, region, *args, **kwargs):
      
      resource_list = self.get_cloud_client().general_boto_call_array(
          boto_call=lambda item: client.get_resources(**item),
          boto_params={"ResourceTypeFilters": ['memorydb']},
          boto_nextkey = "PaginationToken",
          boto_key="ResourceTagMappingList"
      )

      return {
        resource["ResourceARN"].lower():resource["Tags"] for resource in resource_list
      }

  async def __get_clusters(self, client, *args, **kwargs):
    return self.get_cloud_client().general_boto_call_array(
      boto_call=lambda item: client.describe_clusters(**item),
      boto_params={"ShowShardDetails": True},
      boto_nextkey = "NextToken",
      boto_key="Clusters"
    )

  async def _process_account_data_region(self, account, region, resource_groups, loop, *args, **kwargs):
    client = self.get_cloud_client().get_boto_client(client= 'memorydb',  account=account, region=region)
    resourcegroupstaggingapi_client = self.get_cloud_client().get_boto_client(client= 'resourcegroupstaggingapi',  account=account, region=region)

    tasks = {
      "clusters": loop.create_task(self.__get_clusters(client= client)),
      "tags": loop.create_task(self.__get_memorydb_tags(client= resourcegroupstaggingapi_client,  account=account, region=region)),
    }
    
    if len(tasks) > 0:
      await asyncio.wait(tasks.values())

    return {
      "region": region,
      "resource_groups": resource_groups,
      "data": [
        self.get_common().helper_type().dictionary().merge_dictionary([
          {},
          {
            "extra_tags": tasks["tags"].result().get(item["ARN"].lower()),
            "extra_type": "memorydb"
          }, 
          item
        ]) for item in tasks["clusters"].result()
        ]
    }
