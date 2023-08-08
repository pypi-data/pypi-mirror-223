"""
Type annotations for cleanrooms service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanrooms/type_defs/)

Usage::

    ```python
    from types_aiobotocore_cleanrooms.type_defs import AggregateColumnTypeDef

    data: AggregateColumnTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AggregateFunctionNameType,
    AnalysisRuleTypeType,
    CollaborationQueryLogStatusType,
    ConfiguredTableAnalysisRuleTypeType,
    FilterableMemberStatusType,
    JoinOperatorType,
    MemberAbilityType,
    MembershipQueryLogStatusType,
    MembershipStatusType,
    MemberStatusType,
    ParameterTypeType,
    ProtectedQueryStatusType,
    ResultFormatType,
    ScalarFunctionsType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AggregateColumnTypeDef",
    "AggregationConstraintTypeDef",
    "AnalysisParameterTypeDef",
    "AnalysisRuleCustomTypeDef",
    "AnalysisRuleListTypeDef",
    "AnalysisSchemaTypeDef",
    "AnalysisSourceTypeDef",
    "AnalysisTemplateSummaryTypeDef",
    "BatchGetCollaborationAnalysisTemplateErrorTypeDef",
    "BatchGetCollaborationAnalysisTemplateInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchGetSchemaErrorTypeDef",
    "BatchGetSchemaInputRequestTypeDef",
    "CollaborationAnalysisTemplateSummaryTypeDef",
    "CollaborationSummaryTypeDef",
    "DataEncryptionMetadataTypeDef",
    "ColumnTypeDef",
    "ConfiguredTableAssociationSummaryTypeDef",
    "ConfiguredTableAssociationTypeDef",
    "ConfiguredTableSummaryTypeDef",
    "MemberSpecificationTypeDef",
    "CreateConfiguredTableAssociationInputRequestTypeDef",
    "CreateMembershipInputRequestTypeDef",
    "MembershipTypeDef",
    "DeleteAnalysisTemplateInputRequestTypeDef",
    "DeleteCollaborationInputRequestTypeDef",
    "DeleteConfiguredTableAnalysisRuleInputRequestTypeDef",
    "DeleteConfiguredTableAssociationInputRequestTypeDef",
    "DeleteConfiguredTableInputRequestTypeDef",
    "DeleteMemberInputRequestTypeDef",
    "DeleteMembershipInputRequestTypeDef",
    "GetAnalysisTemplateInputRequestTypeDef",
    "GetCollaborationAnalysisTemplateInputRequestTypeDef",
    "GetCollaborationInputRequestTypeDef",
    "GetConfiguredTableAnalysisRuleInputRequestTypeDef",
    "GetConfiguredTableAssociationInputRequestTypeDef",
    "GetConfiguredTableInputRequestTypeDef",
    "GetMembershipInputRequestTypeDef",
    "GetProtectedQueryInputRequestTypeDef",
    "GetSchemaAnalysisRuleInputRequestTypeDef",
    "GetSchemaInputRequestTypeDef",
    "GlueTableReferenceTypeDef",
    "PaginatorConfigTypeDef",
    "ListAnalysisTemplatesInputRequestTypeDef",
    "ListCollaborationAnalysisTemplatesInputRequestTypeDef",
    "ListCollaborationsInputRequestTypeDef",
    "ListConfiguredTableAssociationsInputRequestTypeDef",
    "ListConfiguredTablesInputRequestTypeDef",
    "ListMembersInputRequestTypeDef",
    "MemberSummaryTypeDef",
    "ListMembershipsInputRequestTypeDef",
    "MembershipSummaryTypeDef",
    "ListProtectedQueriesInputRequestTypeDef",
    "ProtectedQuerySummaryTypeDef",
    "ListSchemasInputRequestTypeDef",
    "SchemaSummaryTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ProtectedQueryErrorTypeDef",
    "ProtectedQueryS3OutputConfigurationTypeDef",
    "ProtectedQueryS3OutputTypeDef",
    "ProtectedQuerySQLParametersTypeDef",
    "ProtectedQueryStatisticsTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateAnalysisTemplateInputRequestTypeDef",
    "UpdateCollaborationInputRequestTypeDef",
    "UpdateConfiguredTableAssociationInputRequestTypeDef",
    "UpdateConfiguredTableInputRequestTypeDef",
    "UpdateMembershipInputRequestTypeDef",
    "UpdateProtectedQueryInputRequestTypeDef",
    "AnalysisRuleAggregationTypeDef",
    "AnalysisTemplateTypeDef",
    "CollaborationAnalysisTemplateTypeDef",
    "CreateAnalysisTemplateInputRequestTypeDef",
    "ListAnalysisTemplatesOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListCollaborationAnalysisTemplatesOutputTypeDef",
    "ListCollaborationsOutputTypeDef",
    "CollaborationTypeDef",
    "SchemaTypeDef",
    "ListConfiguredTableAssociationsOutputTypeDef",
    "CreateConfiguredTableAssociationOutputTypeDef",
    "GetConfiguredTableAssociationOutputTypeDef",
    "UpdateConfiguredTableAssociationOutputTypeDef",
    "ListConfiguredTablesOutputTypeDef",
    "CreateCollaborationInputRequestTypeDef",
    "CreateMembershipOutputTypeDef",
    "GetMembershipOutputTypeDef",
    "UpdateMembershipOutputTypeDef",
    "TableReferenceTypeDef",
    "ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef",
    "ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef",
    "ListCollaborationsInputListCollaborationsPaginateTypeDef",
    "ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef",
    "ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef",
    "ListMembersInputListMembersPaginateTypeDef",
    "ListMembershipsInputListMembershipsPaginateTypeDef",
    "ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef",
    "ListSchemasInputListSchemasPaginateTypeDef",
    "ListMembersOutputTypeDef",
    "ListMembershipsOutputTypeDef",
    "ListProtectedQueriesOutputTypeDef",
    "ListSchemasOutputTypeDef",
    "ProtectedQueryOutputConfigurationTypeDef",
    "ProtectedQueryOutputTypeDef",
    "AnalysisRulePolicyV1TypeDef",
    "ConfiguredTableAnalysisRulePolicyV1TypeDef",
    "CreateAnalysisTemplateOutputTypeDef",
    "GetAnalysisTemplateOutputTypeDef",
    "UpdateAnalysisTemplateOutputTypeDef",
    "BatchGetCollaborationAnalysisTemplateOutputTypeDef",
    "GetCollaborationAnalysisTemplateOutputTypeDef",
    "CreateCollaborationOutputTypeDef",
    "GetCollaborationOutputTypeDef",
    "UpdateCollaborationOutputTypeDef",
    "BatchGetSchemaOutputTypeDef",
    "GetSchemaOutputTypeDef",
    "ConfiguredTableTypeDef",
    "CreateConfiguredTableInputRequestTypeDef",
    "ProtectedQueryResultConfigurationTypeDef",
    "ProtectedQueryResultTypeDef",
    "AnalysisRulePolicyTypeDef",
    "ConfiguredTableAnalysisRulePolicyTypeDef",
    "CreateConfiguredTableOutputTypeDef",
    "GetConfiguredTableOutputTypeDef",
    "UpdateConfiguredTableOutputTypeDef",
    "StartProtectedQueryInputRequestTypeDef",
    "ProtectedQueryTypeDef",
    "AnalysisRuleTypeDef",
    "ConfiguredTableAnalysisRuleTypeDef",
    "CreateConfiguredTableAnalysisRuleInputRequestTypeDef",
    "UpdateConfiguredTableAnalysisRuleInputRequestTypeDef",
    "GetProtectedQueryOutputTypeDef",
    "StartProtectedQueryOutputTypeDef",
    "UpdateProtectedQueryOutputTypeDef",
    "GetSchemaAnalysisRuleOutputTypeDef",
    "CreateConfiguredTableAnalysisRuleOutputTypeDef",
    "GetConfiguredTableAnalysisRuleOutputTypeDef",
    "UpdateConfiguredTableAnalysisRuleOutputTypeDef",
)

AggregateColumnTypeDef = TypedDict(
    "AggregateColumnTypeDef",
    {
        "columnNames": Sequence[str],
        "function": AggregateFunctionNameType,
    },
)

AggregationConstraintTypeDef = TypedDict(
    "AggregationConstraintTypeDef",
    {
        "columnName": str,
        "minimum": int,
        "type": Literal["COUNT_DISTINCT"],
    },
)

_RequiredAnalysisParameterTypeDef = TypedDict(
    "_RequiredAnalysisParameterTypeDef",
    {
        "name": str,
        "type": ParameterTypeType,
    },
)
_OptionalAnalysisParameterTypeDef = TypedDict(
    "_OptionalAnalysisParameterTypeDef",
    {
        "defaultValue": str,
    },
    total=False,
)

class AnalysisParameterTypeDef(
    _RequiredAnalysisParameterTypeDef, _OptionalAnalysisParameterTypeDef
):
    pass

_RequiredAnalysisRuleCustomTypeDef = TypedDict(
    "_RequiredAnalysisRuleCustomTypeDef",
    {
        "allowedAnalyses": Sequence[str],
    },
)
_OptionalAnalysisRuleCustomTypeDef = TypedDict(
    "_OptionalAnalysisRuleCustomTypeDef",
    {
        "allowedAnalysisProviders": Sequence[str],
    },
    total=False,
)

class AnalysisRuleCustomTypeDef(
    _RequiredAnalysisRuleCustomTypeDef, _OptionalAnalysisRuleCustomTypeDef
):
    pass

_RequiredAnalysisRuleListTypeDef = TypedDict(
    "_RequiredAnalysisRuleListTypeDef",
    {
        "joinColumns": Sequence[str],
        "listColumns": Sequence[str],
    },
)
_OptionalAnalysisRuleListTypeDef = TypedDict(
    "_OptionalAnalysisRuleListTypeDef",
    {
        "allowedJoinOperators": Sequence[JoinOperatorType],
    },
    total=False,
)

class AnalysisRuleListTypeDef(_RequiredAnalysisRuleListTypeDef, _OptionalAnalysisRuleListTypeDef):
    pass

AnalysisSchemaTypeDef = TypedDict(
    "AnalysisSchemaTypeDef",
    {
        "referencedTables": List[str],
    },
    total=False,
)

AnalysisSourceTypeDef = TypedDict(
    "AnalysisSourceTypeDef",
    {
        "text": str,
    },
    total=False,
)

_RequiredAnalysisTemplateSummaryTypeDef = TypedDict(
    "_RequiredAnalysisTemplateSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "name": str,
        "updateTime": datetime,
        "membershipArn": str,
        "membershipId": str,
        "collaborationArn": str,
        "collaborationId": str,
    },
)
_OptionalAnalysisTemplateSummaryTypeDef = TypedDict(
    "_OptionalAnalysisTemplateSummaryTypeDef",
    {
        "description": str,
    },
    total=False,
)

class AnalysisTemplateSummaryTypeDef(
    _RequiredAnalysisTemplateSummaryTypeDef, _OptionalAnalysisTemplateSummaryTypeDef
):
    pass

BatchGetCollaborationAnalysisTemplateErrorTypeDef = TypedDict(
    "BatchGetCollaborationAnalysisTemplateErrorTypeDef",
    {
        "arn": str,
        "code": str,
        "message": str,
    },
)

BatchGetCollaborationAnalysisTemplateInputRequestTypeDef = TypedDict(
    "BatchGetCollaborationAnalysisTemplateInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "analysisTemplateArns": Sequence[str],
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

BatchGetSchemaErrorTypeDef = TypedDict(
    "BatchGetSchemaErrorTypeDef",
    {
        "name": str,
        "code": str,
        "message": str,
    },
)

BatchGetSchemaInputRequestTypeDef = TypedDict(
    "BatchGetSchemaInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "names": Sequence[str],
    },
)

_RequiredCollaborationAnalysisTemplateSummaryTypeDef = TypedDict(
    "_RequiredCollaborationAnalysisTemplateSummaryTypeDef",
    {
        "arn": str,
        "createTime": datetime,
        "id": str,
        "name": str,
        "updateTime": datetime,
        "collaborationArn": str,
        "collaborationId": str,
        "creatorAccountId": str,
    },
)
_OptionalCollaborationAnalysisTemplateSummaryTypeDef = TypedDict(
    "_OptionalCollaborationAnalysisTemplateSummaryTypeDef",
    {
        "description": str,
    },
    total=False,
)

class CollaborationAnalysisTemplateSummaryTypeDef(
    _RequiredCollaborationAnalysisTemplateSummaryTypeDef,
    _OptionalCollaborationAnalysisTemplateSummaryTypeDef,
):
    pass

_RequiredCollaborationSummaryTypeDef = TypedDict(
    "_RequiredCollaborationSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "creatorAccountId": str,
        "creatorDisplayName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "memberStatus": MemberStatusType,
    },
)
_OptionalCollaborationSummaryTypeDef = TypedDict(
    "_OptionalCollaborationSummaryTypeDef",
    {
        "membershipId": str,
        "membershipArn": str,
    },
    total=False,
)

class CollaborationSummaryTypeDef(
    _RequiredCollaborationSummaryTypeDef, _OptionalCollaborationSummaryTypeDef
):
    pass

DataEncryptionMetadataTypeDef = TypedDict(
    "DataEncryptionMetadataTypeDef",
    {
        "allowCleartext": bool,
        "allowDuplicates": bool,
        "allowJoinsOnColumnsWithDifferentNames": bool,
        "preserveNulls": bool,
    },
)

ColumnTypeDef = TypedDict(
    "ColumnTypeDef",
    {
        "name": str,
        "type": str,
    },
)

ConfiguredTableAssociationSummaryTypeDef = TypedDict(
    "ConfiguredTableAssociationSummaryTypeDef",
    {
        "configuredTableId": str,
        "membershipId": str,
        "membershipArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "id": str,
        "arn": str,
    },
)

_RequiredConfiguredTableAssociationTypeDef = TypedDict(
    "_RequiredConfiguredTableAssociationTypeDef",
    {
        "arn": str,
        "id": str,
        "configuredTableId": str,
        "configuredTableArn": str,
        "membershipId": str,
        "membershipArn": str,
        "roleArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
    },
)
_OptionalConfiguredTableAssociationTypeDef = TypedDict(
    "_OptionalConfiguredTableAssociationTypeDef",
    {
        "description": str,
    },
    total=False,
)

class ConfiguredTableAssociationTypeDef(
    _RequiredConfiguredTableAssociationTypeDef, _OptionalConfiguredTableAssociationTypeDef
):
    pass

ConfiguredTableSummaryTypeDef = TypedDict(
    "ConfiguredTableSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "analysisRuleTypes": List[ConfiguredTableAnalysisRuleTypeType],
        "analysisMethod": Literal["DIRECT_QUERY"],
    },
)

MemberSpecificationTypeDef = TypedDict(
    "MemberSpecificationTypeDef",
    {
        "accountId": str,
        "memberAbilities": Sequence[MemberAbilityType],
        "displayName": str,
    },
)

_RequiredCreateConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "_RequiredCreateConfiguredTableAssociationInputRequestTypeDef",
    {
        "name": str,
        "membershipIdentifier": str,
        "configuredTableIdentifier": str,
        "roleArn": str,
    },
)
_OptionalCreateConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "_OptionalCreateConfiguredTableAssociationInputRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateConfiguredTableAssociationInputRequestTypeDef(
    _RequiredCreateConfiguredTableAssociationInputRequestTypeDef,
    _OptionalCreateConfiguredTableAssociationInputRequestTypeDef,
):
    pass

_RequiredCreateMembershipInputRequestTypeDef = TypedDict(
    "_RequiredCreateMembershipInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "queryLogStatus": MembershipQueryLogStatusType,
    },
)
_OptionalCreateMembershipInputRequestTypeDef = TypedDict(
    "_OptionalCreateMembershipInputRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateMembershipInputRequestTypeDef(
    _RequiredCreateMembershipInputRequestTypeDef, _OptionalCreateMembershipInputRequestTypeDef
):
    pass

MembershipTypeDef = TypedDict(
    "MembershipTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "collaborationCreatorAccountId": str,
        "collaborationCreatorDisplayName": str,
        "collaborationName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "status": MembershipStatusType,
        "memberAbilities": List[MemberAbilityType],
        "queryLogStatus": MembershipQueryLogStatusType,
    },
)

DeleteAnalysisTemplateInputRequestTypeDef = TypedDict(
    "DeleteAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "analysisTemplateIdentifier": str,
    },
)

DeleteCollaborationInputRequestTypeDef = TypedDict(
    "DeleteCollaborationInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)

DeleteConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "DeleteConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
    },
)

DeleteConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "DeleteConfiguredTableAssociationInputRequestTypeDef",
    {
        "configuredTableAssociationIdentifier": str,
        "membershipIdentifier": str,
    },
)

DeleteConfiguredTableInputRequestTypeDef = TypedDict(
    "DeleteConfiguredTableInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
    },
)

DeleteMemberInputRequestTypeDef = TypedDict(
    "DeleteMemberInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "accountId": str,
    },
)

DeleteMembershipInputRequestTypeDef = TypedDict(
    "DeleteMembershipInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)

GetAnalysisTemplateInputRequestTypeDef = TypedDict(
    "GetAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "analysisTemplateIdentifier": str,
    },
)

GetCollaborationAnalysisTemplateInputRequestTypeDef = TypedDict(
    "GetCollaborationAnalysisTemplateInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "analysisTemplateArn": str,
    },
)

GetCollaborationInputRequestTypeDef = TypedDict(
    "GetCollaborationInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)

GetConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "GetConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
    },
)

GetConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "GetConfiguredTableAssociationInputRequestTypeDef",
    {
        "configuredTableAssociationIdentifier": str,
        "membershipIdentifier": str,
    },
)

GetConfiguredTableInputRequestTypeDef = TypedDict(
    "GetConfiguredTableInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
    },
)

GetMembershipInputRequestTypeDef = TypedDict(
    "GetMembershipInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)

GetProtectedQueryInputRequestTypeDef = TypedDict(
    "GetProtectedQueryInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "protectedQueryIdentifier": str,
    },
)

GetSchemaAnalysisRuleInputRequestTypeDef = TypedDict(
    "GetSchemaAnalysisRuleInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "name": str,
        "type": AnalysisRuleTypeType,
    },
)

GetSchemaInputRequestTypeDef = TypedDict(
    "GetSchemaInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
        "name": str,
    },
)

GlueTableReferenceTypeDef = TypedDict(
    "GlueTableReferenceTypeDef",
    {
        "tableName": str,
        "databaseName": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListAnalysisTemplatesInputRequestTypeDef = TypedDict(
    "_RequiredListAnalysisTemplatesInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)
_OptionalListAnalysisTemplatesInputRequestTypeDef = TypedDict(
    "_OptionalListAnalysisTemplatesInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListAnalysisTemplatesInputRequestTypeDef(
    _RequiredListAnalysisTemplatesInputRequestTypeDef,
    _OptionalListAnalysisTemplatesInputRequestTypeDef,
):
    pass

_RequiredListCollaborationAnalysisTemplatesInputRequestTypeDef = TypedDict(
    "_RequiredListCollaborationAnalysisTemplatesInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
_OptionalListCollaborationAnalysisTemplatesInputRequestTypeDef = TypedDict(
    "_OptionalListCollaborationAnalysisTemplatesInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListCollaborationAnalysisTemplatesInputRequestTypeDef(
    _RequiredListCollaborationAnalysisTemplatesInputRequestTypeDef,
    _OptionalListCollaborationAnalysisTemplatesInputRequestTypeDef,
):
    pass

ListCollaborationsInputRequestTypeDef = TypedDict(
    "ListCollaborationsInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "memberStatus": FilterableMemberStatusType,
    },
    total=False,
)

_RequiredListConfiguredTableAssociationsInputRequestTypeDef = TypedDict(
    "_RequiredListConfiguredTableAssociationsInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)
_OptionalListConfiguredTableAssociationsInputRequestTypeDef = TypedDict(
    "_OptionalListConfiguredTableAssociationsInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListConfiguredTableAssociationsInputRequestTypeDef(
    _RequiredListConfiguredTableAssociationsInputRequestTypeDef,
    _OptionalListConfiguredTableAssociationsInputRequestTypeDef,
):
    pass

ListConfiguredTablesInputRequestTypeDef = TypedDict(
    "ListConfiguredTablesInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

_RequiredListMembersInputRequestTypeDef = TypedDict(
    "_RequiredListMembersInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
_OptionalListMembersInputRequestTypeDef = TypedDict(
    "_OptionalListMembersInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListMembersInputRequestTypeDef(
    _RequiredListMembersInputRequestTypeDef, _OptionalListMembersInputRequestTypeDef
):
    pass

_RequiredMemberSummaryTypeDef = TypedDict(
    "_RequiredMemberSummaryTypeDef",
    {
        "accountId": str,
        "status": MemberStatusType,
        "displayName": str,
        "abilities": List[MemberAbilityType],
        "createTime": datetime,
        "updateTime": datetime,
    },
)
_OptionalMemberSummaryTypeDef = TypedDict(
    "_OptionalMemberSummaryTypeDef",
    {
        "membershipId": str,
        "membershipArn": str,
    },
    total=False,
)

class MemberSummaryTypeDef(_RequiredMemberSummaryTypeDef, _OptionalMemberSummaryTypeDef):
    pass

ListMembershipsInputRequestTypeDef = TypedDict(
    "ListMembershipsInputRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
        "status": MembershipStatusType,
    },
    total=False,
)

MembershipSummaryTypeDef = TypedDict(
    "MembershipSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationArn": str,
        "collaborationId": str,
        "collaborationCreatorAccountId": str,
        "collaborationCreatorDisplayName": str,
        "collaborationName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "status": MembershipStatusType,
        "memberAbilities": List[MemberAbilityType],
    },
)

_RequiredListProtectedQueriesInputRequestTypeDef = TypedDict(
    "_RequiredListProtectedQueriesInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)
_OptionalListProtectedQueriesInputRequestTypeDef = TypedDict(
    "_OptionalListProtectedQueriesInputRequestTypeDef",
    {
        "status": ProtectedQueryStatusType,
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListProtectedQueriesInputRequestTypeDef(
    _RequiredListProtectedQueriesInputRequestTypeDef,
    _OptionalListProtectedQueriesInputRequestTypeDef,
):
    pass

ProtectedQuerySummaryTypeDef = TypedDict(
    "ProtectedQuerySummaryTypeDef",
    {
        "id": str,
        "membershipId": str,
        "membershipArn": str,
        "createTime": datetime,
        "status": ProtectedQueryStatusType,
    },
)

_RequiredListSchemasInputRequestTypeDef = TypedDict(
    "_RequiredListSchemasInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
_OptionalListSchemasInputRequestTypeDef = TypedDict(
    "_OptionalListSchemasInputRequestTypeDef",
    {
        "schemaType": Literal["TABLE"],
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListSchemasInputRequestTypeDef(
    _RequiredListSchemasInputRequestTypeDef, _OptionalListSchemasInputRequestTypeDef
):
    pass

_RequiredSchemaSummaryTypeDef = TypedDict(
    "_RequiredSchemaSummaryTypeDef",
    {
        "name": str,
        "type": Literal["TABLE"],
        "creatorAccountId": str,
        "createTime": datetime,
        "updateTime": datetime,
        "collaborationId": str,
        "collaborationArn": str,
        "analysisRuleTypes": List[AnalysisRuleTypeType],
    },
)
_OptionalSchemaSummaryTypeDef = TypedDict(
    "_OptionalSchemaSummaryTypeDef",
    {
        "analysisMethod": Literal["DIRECT_QUERY"],
    },
    total=False,
)

class SchemaSummaryTypeDef(_RequiredSchemaSummaryTypeDef, _OptionalSchemaSummaryTypeDef):
    pass

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ProtectedQueryErrorTypeDef = TypedDict(
    "ProtectedQueryErrorTypeDef",
    {
        "message": str,
        "code": str,
    },
)

_RequiredProtectedQueryS3OutputConfigurationTypeDef = TypedDict(
    "_RequiredProtectedQueryS3OutputConfigurationTypeDef",
    {
        "resultFormat": ResultFormatType,
        "bucket": str,
    },
)
_OptionalProtectedQueryS3OutputConfigurationTypeDef = TypedDict(
    "_OptionalProtectedQueryS3OutputConfigurationTypeDef",
    {
        "keyPrefix": str,
    },
    total=False,
)

class ProtectedQueryS3OutputConfigurationTypeDef(
    _RequiredProtectedQueryS3OutputConfigurationTypeDef,
    _OptionalProtectedQueryS3OutputConfigurationTypeDef,
):
    pass

ProtectedQueryS3OutputTypeDef = TypedDict(
    "ProtectedQueryS3OutputTypeDef",
    {
        "location": str,
    },
)

ProtectedQuerySQLParametersTypeDef = TypedDict(
    "ProtectedQuerySQLParametersTypeDef",
    {
        "queryString": str,
        "analysisTemplateArn": str,
        "parameters": Dict[str, str],
    },
    total=False,
)

ProtectedQueryStatisticsTypeDef = TypedDict(
    "ProtectedQueryStatisticsTypeDef",
    {
        "totalDurationInMillis": int,
    },
    total=False,
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateAnalysisTemplateInputRequestTypeDef = TypedDict(
    "_RequiredUpdateAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "analysisTemplateIdentifier": str,
    },
)
_OptionalUpdateAnalysisTemplateInputRequestTypeDef = TypedDict(
    "_OptionalUpdateAnalysisTemplateInputRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class UpdateAnalysisTemplateInputRequestTypeDef(
    _RequiredUpdateAnalysisTemplateInputRequestTypeDef,
    _OptionalUpdateAnalysisTemplateInputRequestTypeDef,
):
    pass

_RequiredUpdateCollaborationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateCollaborationInputRequestTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
_OptionalUpdateCollaborationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateCollaborationInputRequestTypeDef",
    {
        "name": str,
        "description": str,
    },
    total=False,
)

class UpdateCollaborationInputRequestTypeDef(
    _RequiredUpdateCollaborationInputRequestTypeDef, _OptionalUpdateCollaborationInputRequestTypeDef
):
    pass

_RequiredUpdateConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "_RequiredUpdateConfiguredTableAssociationInputRequestTypeDef",
    {
        "configuredTableAssociationIdentifier": str,
        "membershipIdentifier": str,
    },
)
_OptionalUpdateConfiguredTableAssociationInputRequestTypeDef = TypedDict(
    "_OptionalUpdateConfiguredTableAssociationInputRequestTypeDef",
    {
        "description": str,
        "roleArn": str,
    },
    total=False,
)

class UpdateConfiguredTableAssociationInputRequestTypeDef(
    _RequiredUpdateConfiguredTableAssociationInputRequestTypeDef,
    _OptionalUpdateConfiguredTableAssociationInputRequestTypeDef,
):
    pass

_RequiredUpdateConfiguredTableInputRequestTypeDef = TypedDict(
    "_RequiredUpdateConfiguredTableInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
    },
)
_OptionalUpdateConfiguredTableInputRequestTypeDef = TypedDict(
    "_OptionalUpdateConfiguredTableInputRequestTypeDef",
    {
        "name": str,
        "description": str,
    },
    total=False,
)

class UpdateConfiguredTableInputRequestTypeDef(
    _RequiredUpdateConfiguredTableInputRequestTypeDef,
    _OptionalUpdateConfiguredTableInputRequestTypeDef,
):
    pass

_RequiredUpdateMembershipInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMembershipInputRequestTypeDef",
    {
        "membershipIdentifier": str,
    },
)
_OptionalUpdateMembershipInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMembershipInputRequestTypeDef",
    {
        "queryLogStatus": MembershipQueryLogStatusType,
    },
    total=False,
)

class UpdateMembershipInputRequestTypeDef(
    _RequiredUpdateMembershipInputRequestTypeDef, _OptionalUpdateMembershipInputRequestTypeDef
):
    pass

UpdateProtectedQueryInputRequestTypeDef = TypedDict(
    "UpdateProtectedQueryInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "protectedQueryIdentifier": str,
        "targetStatus": Literal["CANCELLED"],
    },
)

_RequiredAnalysisRuleAggregationTypeDef = TypedDict(
    "_RequiredAnalysisRuleAggregationTypeDef",
    {
        "aggregateColumns": Sequence[AggregateColumnTypeDef],
        "joinColumns": Sequence[str],
        "dimensionColumns": Sequence[str],
        "scalarFunctions": Sequence[ScalarFunctionsType],
        "outputConstraints": Sequence[AggregationConstraintTypeDef],
    },
)
_OptionalAnalysisRuleAggregationTypeDef = TypedDict(
    "_OptionalAnalysisRuleAggregationTypeDef",
    {
        "joinRequired": Literal["QUERY_RUNNER"],
        "allowedJoinOperators": Sequence[JoinOperatorType],
    },
    total=False,
)

class AnalysisRuleAggregationTypeDef(
    _RequiredAnalysisRuleAggregationTypeDef, _OptionalAnalysisRuleAggregationTypeDef
):
    pass

_RequiredAnalysisTemplateTypeDef = TypedDict(
    "_RequiredAnalysisTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "membershipId": str,
        "membershipArn": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "schema": AnalysisSchemaTypeDef,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
    },
)
_OptionalAnalysisTemplateTypeDef = TypedDict(
    "_OptionalAnalysisTemplateTypeDef",
    {
        "description": str,
        "analysisParameters": List[AnalysisParameterTypeDef],
    },
    total=False,
)

class AnalysisTemplateTypeDef(_RequiredAnalysisTemplateTypeDef, _OptionalAnalysisTemplateTypeDef):
    pass

_RequiredCollaborationAnalysisTemplateTypeDef = TypedDict(
    "_RequiredCollaborationAnalysisTemplateTypeDef",
    {
        "id": str,
        "arn": str,
        "collaborationId": str,
        "collaborationArn": str,
        "creatorAccountId": str,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "schema": AnalysisSchemaTypeDef,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
    },
)
_OptionalCollaborationAnalysisTemplateTypeDef = TypedDict(
    "_OptionalCollaborationAnalysisTemplateTypeDef",
    {
        "description": str,
        "analysisParameters": List[AnalysisParameterTypeDef],
    },
    total=False,
)

class CollaborationAnalysisTemplateTypeDef(
    _RequiredCollaborationAnalysisTemplateTypeDef, _OptionalCollaborationAnalysisTemplateTypeDef
):
    pass

_RequiredCreateAnalysisTemplateInputRequestTypeDef = TypedDict(
    "_RequiredCreateAnalysisTemplateInputRequestTypeDef",
    {
        "membershipIdentifier": str,
        "name": str,
        "format": Literal["SQL"],
        "source": AnalysisSourceTypeDef,
    },
)
_OptionalCreateAnalysisTemplateInputRequestTypeDef = TypedDict(
    "_OptionalCreateAnalysisTemplateInputRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
        "analysisParameters": Sequence[AnalysisParameterTypeDef],
    },
    total=False,
)

class CreateAnalysisTemplateInputRequestTypeDef(
    _RequiredCreateAnalysisTemplateInputRequestTypeDef,
    _OptionalCreateAnalysisTemplateInputRequestTypeDef,
):
    pass

ListAnalysisTemplatesOutputTypeDef = TypedDict(
    "ListAnalysisTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "analysisTemplateSummaries": List[AnalysisTemplateSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCollaborationAnalysisTemplatesOutputTypeDef = TypedDict(
    "ListCollaborationAnalysisTemplatesOutputTypeDef",
    {
        "nextToken": str,
        "collaborationAnalysisTemplateSummaries": List[CollaborationAnalysisTemplateSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCollaborationsOutputTypeDef = TypedDict(
    "ListCollaborationsOutputTypeDef",
    {
        "nextToken": str,
        "collaborationList": List[CollaborationSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCollaborationTypeDef = TypedDict(
    "_RequiredCollaborationTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "creatorAccountId": str,
        "creatorDisplayName": str,
        "createTime": datetime,
        "updateTime": datetime,
        "memberStatus": MemberStatusType,
        "queryLogStatus": CollaborationQueryLogStatusType,
    },
)
_OptionalCollaborationTypeDef = TypedDict(
    "_OptionalCollaborationTypeDef",
    {
        "description": str,
        "membershipId": str,
        "membershipArn": str,
        "dataEncryptionMetadata": DataEncryptionMetadataTypeDef,
    },
    total=False,
)

class CollaborationTypeDef(_RequiredCollaborationTypeDef, _OptionalCollaborationTypeDef):
    pass

_RequiredSchemaTypeDef = TypedDict(
    "_RequiredSchemaTypeDef",
    {
        "columns": List[ColumnTypeDef],
        "partitionKeys": List[ColumnTypeDef],
        "analysisRuleTypes": List[AnalysisRuleTypeType],
        "creatorAccountId": str,
        "name": str,
        "collaborationId": str,
        "collaborationArn": str,
        "description": str,
        "createTime": datetime,
        "updateTime": datetime,
        "type": Literal["TABLE"],
    },
)
_OptionalSchemaTypeDef = TypedDict(
    "_OptionalSchemaTypeDef",
    {
        "analysisMethod": Literal["DIRECT_QUERY"],
    },
    total=False,
)

class SchemaTypeDef(_RequiredSchemaTypeDef, _OptionalSchemaTypeDef):
    pass

ListConfiguredTableAssociationsOutputTypeDef = TypedDict(
    "ListConfiguredTableAssociationsOutputTypeDef",
    {
        "configuredTableAssociationSummaries": List[ConfiguredTableAssociationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConfiguredTableAssociationOutputTypeDef = TypedDict(
    "CreateConfiguredTableAssociationOutputTypeDef",
    {
        "configuredTableAssociation": ConfiguredTableAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConfiguredTableAssociationOutputTypeDef = TypedDict(
    "GetConfiguredTableAssociationOutputTypeDef",
    {
        "configuredTableAssociation": ConfiguredTableAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConfiguredTableAssociationOutputTypeDef = TypedDict(
    "UpdateConfiguredTableAssociationOutputTypeDef",
    {
        "configuredTableAssociation": ConfiguredTableAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfiguredTablesOutputTypeDef = TypedDict(
    "ListConfiguredTablesOutputTypeDef",
    {
        "configuredTableSummaries": List[ConfiguredTableSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateCollaborationInputRequestTypeDef = TypedDict(
    "_RequiredCreateCollaborationInputRequestTypeDef",
    {
        "members": Sequence[MemberSpecificationTypeDef],
        "name": str,
        "description": str,
        "creatorMemberAbilities": Sequence[MemberAbilityType],
        "creatorDisplayName": str,
        "queryLogStatus": CollaborationQueryLogStatusType,
    },
)
_OptionalCreateCollaborationInputRequestTypeDef = TypedDict(
    "_OptionalCreateCollaborationInputRequestTypeDef",
    {
        "dataEncryptionMetadata": DataEncryptionMetadataTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateCollaborationInputRequestTypeDef(
    _RequiredCreateCollaborationInputRequestTypeDef, _OptionalCreateCollaborationInputRequestTypeDef
):
    pass

CreateMembershipOutputTypeDef = TypedDict(
    "CreateMembershipOutputTypeDef",
    {
        "membership": MembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMembershipOutputTypeDef = TypedDict(
    "GetMembershipOutputTypeDef",
    {
        "membership": MembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMembershipOutputTypeDef = TypedDict(
    "UpdateMembershipOutputTypeDef",
    {
        "membership": MembershipTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TableReferenceTypeDef = TypedDict(
    "TableReferenceTypeDef",
    {
        "glue": GlueTableReferenceTypeDef,
    },
    total=False,
)

_RequiredListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef = TypedDict(
    "_RequiredListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef",
    {
        "membershipIdentifier": str,
    },
)
_OptionalListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef = TypedDict(
    "_OptionalListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef(
    _RequiredListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef,
    _OptionalListAnalysisTemplatesInputListAnalysisTemplatesPaginateTypeDef,
):
    pass

_RequiredListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef = TypedDict(
    "_RequiredListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
_OptionalListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef = TypedDict(
    "_OptionalListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef(
    _RequiredListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef,
    _OptionalListCollaborationAnalysisTemplatesInputListCollaborationAnalysisTemplatesPaginateTypeDef,
):
    pass

ListCollaborationsInputListCollaborationsPaginateTypeDef = TypedDict(
    "ListCollaborationsInputListCollaborationsPaginateTypeDef",
    {
        "memberStatus": FilterableMemberStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef = TypedDict(
    "_RequiredListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef",
    {
        "membershipIdentifier": str,
    },
)
_OptionalListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef = TypedDict(
    "_OptionalListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef(
    _RequiredListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef,
    _OptionalListConfiguredTableAssociationsInputListConfiguredTableAssociationsPaginateTypeDef,
):
    pass

ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef = TypedDict(
    "ListConfiguredTablesInputListConfiguredTablesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListMembersInputListMembersPaginateTypeDef = TypedDict(
    "_RequiredListMembersInputListMembersPaginateTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
_OptionalListMembersInputListMembersPaginateTypeDef = TypedDict(
    "_OptionalListMembersInputListMembersPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListMembersInputListMembersPaginateTypeDef(
    _RequiredListMembersInputListMembersPaginateTypeDef,
    _OptionalListMembersInputListMembersPaginateTypeDef,
):
    pass

ListMembershipsInputListMembershipsPaginateTypeDef = TypedDict(
    "ListMembershipsInputListMembershipsPaginateTypeDef",
    {
        "status": MembershipStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListProtectedQueriesInputListProtectedQueriesPaginateTypeDef = TypedDict(
    "_RequiredListProtectedQueriesInputListProtectedQueriesPaginateTypeDef",
    {
        "membershipIdentifier": str,
    },
)
_OptionalListProtectedQueriesInputListProtectedQueriesPaginateTypeDef = TypedDict(
    "_OptionalListProtectedQueriesInputListProtectedQueriesPaginateTypeDef",
    {
        "status": ProtectedQueryStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListProtectedQueriesInputListProtectedQueriesPaginateTypeDef(
    _RequiredListProtectedQueriesInputListProtectedQueriesPaginateTypeDef,
    _OptionalListProtectedQueriesInputListProtectedQueriesPaginateTypeDef,
):
    pass

_RequiredListSchemasInputListSchemasPaginateTypeDef = TypedDict(
    "_RequiredListSchemasInputListSchemasPaginateTypeDef",
    {
        "collaborationIdentifier": str,
    },
)
_OptionalListSchemasInputListSchemasPaginateTypeDef = TypedDict(
    "_OptionalListSchemasInputListSchemasPaginateTypeDef",
    {
        "schemaType": Literal["TABLE"],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListSchemasInputListSchemasPaginateTypeDef(
    _RequiredListSchemasInputListSchemasPaginateTypeDef,
    _OptionalListSchemasInputListSchemasPaginateTypeDef,
):
    pass

ListMembersOutputTypeDef = TypedDict(
    "ListMembersOutputTypeDef",
    {
        "nextToken": str,
        "memberSummaries": List[MemberSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMembershipsOutputTypeDef = TypedDict(
    "ListMembershipsOutputTypeDef",
    {
        "nextToken": str,
        "membershipSummaries": List[MembershipSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProtectedQueriesOutputTypeDef = TypedDict(
    "ListProtectedQueriesOutputTypeDef",
    {
        "nextToken": str,
        "protectedQueries": List[ProtectedQuerySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchemasOutputTypeDef = TypedDict(
    "ListSchemasOutputTypeDef",
    {
        "schemaSummaries": List[SchemaSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProtectedQueryOutputConfigurationTypeDef = TypedDict(
    "ProtectedQueryOutputConfigurationTypeDef",
    {
        "s3": ProtectedQueryS3OutputConfigurationTypeDef,
    },
    total=False,
)

ProtectedQueryOutputTypeDef = TypedDict(
    "ProtectedQueryOutputTypeDef",
    {
        "s3": ProtectedQueryS3OutputTypeDef,
    },
    total=False,
)

AnalysisRulePolicyV1TypeDef = TypedDict(
    "AnalysisRulePolicyV1TypeDef",
    {
        "list": AnalysisRuleListTypeDef,
        "aggregation": AnalysisRuleAggregationTypeDef,
        "custom": AnalysisRuleCustomTypeDef,
    },
    total=False,
)

ConfiguredTableAnalysisRulePolicyV1TypeDef = TypedDict(
    "ConfiguredTableAnalysisRulePolicyV1TypeDef",
    {
        "list": AnalysisRuleListTypeDef,
        "aggregation": AnalysisRuleAggregationTypeDef,
        "custom": AnalysisRuleCustomTypeDef,
    },
    total=False,
)

CreateAnalysisTemplateOutputTypeDef = TypedDict(
    "CreateAnalysisTemplateOutputTypeDef",
    {
        "analysisTemplate": AnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAnalysisTemplateOutputTypeDef = TypedDict(
    "GetAnalysisTemplateOutputTypeDef",
    {
        "analysisTemplate": AnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAnalysisTemplateOutputTypeDef = TypedDict(
    "UpdateAnalysisTemplateOutputTypeDef",
    {
        "analysisTemplate": AnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetCollaborationAnalysisTemplateOutputTypeDef = TypedDict(
    "BatchGetCollaborationAnalysisTemplateOutputTypeDef",
    {
        "collaborationAnalysisTemplates": List[CollaborationAnalysisTemplateTypeDef],
        "errors": List[BatchGetCollaborationAnalysisTemplateErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCollaborationAnalysisTemplateOutputTypeDef = TypedDict(
    "GetCollaborationAnalysisTemplateOutputTypeDef",
    {
        "collaborationAnalysisTemplate": CollaborationAnalysisTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCollaborationOutputTypeDef = TypedDict(
    "CreateCollaborationOutputTypeDef",
    {
        "collaboration": CollaborationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCollaborationOutputTypeDef = TypedDict(
    "GetCollaborationOutputTypeDef",
    {
        "collaboration": CollaborationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCollaborationOutputTypeDef = TypedDict(
    "UpdateCollaborationOutputTypeDef",
    {
        "collaboration": CollaborationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetSchemaOutputTypeDef = TypedDict(
    "BatchGetSchemaOutputTypeDef",
    {
        "schemas": List[SchemaTypeDef],
        "errors": List[BatchGetSchemaErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaOutputTypeDef = TypedDict(
    "GetSchemaOutputTypeDef",
    {
        "schema": SchemaTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredConfiguredTableTypeDef = TypedDict(
    "_RequiredConfiguredTableTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "tableReference": TableReferenceTypeDef,
        "createTime": datetime,
        "updateTime": datetime,
        "analysisRuleTypes": List[ConfiguredTableAnalysisRuleTypeType],
        "analysisMethod": Literal["DIRECT_QUERY"],
        "allowedColumns": List[str],
    },
)
_OptionalConfiguredTableTypeDef = TypedDict(
    "_OptionalConfiguredTableTypeDef",
    {
        "description": str,
    },
    total=False,
)

class ConfiguredTableTypeDef(_RequiredConfiguredTableTypeDef, _OptionalConfiguredTableTypeDef):
    pass

_RequiredCreateConfiguredTableInputRequestTypeDef = TypedDict(
    "_RequiredCreateConfiguredTableInputRequestTypeDef",
    {
        "name": str,
        "tableReference": TableReferenceTypeDef,
        "allowedColumns": Sequence[str],
        "analysisMethod": Literal["DIRECT_QUERY"],
    },
)
_OptionalCreateConfiguredTableInputRequestTypeDef = TypedDict(
    "_OptionalCreateConfiguredTableInputRequestTypeDef",
    {
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateConfiguredTableInputRequestTypeDef(
    _RequiredCreateConfiguredTableInputRequestTypeDef,
    _OptionalCreateConfiguredTableInputRequestTypeDef,
):
    pass

ProtectedQueryResultConfigurationTypeDef = TypedDict(
    "ProtectedQueryResultConfigurationTypeDef",
    {
        "outputConfiguration": ProtectedQueryOutputConfigurationTypeDef,
    },
)

ProtectedQueryResultTypeDef = TypedDict(
    "ProtectedQueryResultTypeDef",
    {
        "output": ProtectedQueryOutputTypeDef,
    },
)

AnalysisRulePolicyTypeDef = TypedDict(
    "AnalysisRulePolicyTypeDef",
    {
        "v1": AnalysisRulePolicyV1TypeDef,
    },
    total=False,
)

ConfiguredTableAnalysisRulePolicyTypeDef = TypedDict(
    "ConfiguredTableAnalysisRulePolicyTypeDef",
    {
        "v1": ConfiguredTableAnalysisRulePolicyV1TypeDef,
    },
    total=False,
)

CreateConfiguredTableOutputTypeDef = TypedDict(
    "CreateConfiguredTableOutputTypeDef",
    {
        "configuredTable": ConfiguredTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConfiguredTableOutputTypeDef = TypedDict(
    "GetConfiguredTableOutputTypeDef",
    {
        "configuredTable": ConfiguredTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConfiguredTableOutputTypeDef = TypedDict(
    "UpdateConfiguredTableOutputTypeDef",
    {
        "configuredTable": ConfiguredTableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartProtectedQueryInputRequestTypeDef = TypedDict(
    "StartProtectedQueryInputRequestTypeDef",
    {
        "type": Literal["SQL"],
        "membershipIdentifier": str,
        "sqlParameters": ProtectedQuerySQLParametersTypeDef,
        "resultConfiguration": ProtectedQueryResultConfigurationTypeDef,
    },
)

_RequiredProtectedQueryTypeDef = TypedDict(
    "_RequiredProtectedQueryTypeDef",
    {
        "id": str,
        "membershipId": str,
        "membershipArn": str,
        "createTime": datetime,
        "sqlParameters": ProtectedQuerySQLParametersTypeDef,
        "status": ProtectedQueryStatusType,
        "resultConfiguration": ProtectedQueryResultConfigurationTypeDef,
    },
)
_OptionalProtectedQueryTypeDef = TypedDict(
    "_OptionalProtectedQueryTypeDef",
    {
        "statistics": ProtectedQueryStatisticsTypeDef,
        "result": ProtectedQueryResultTypeDef,
        "error": ProtectedQueryErrorTypeDef,
    },
    total=False,
)

class ProtectedQueryTypeDef(_RequiredProtectedQueryTypeDef, _OptionalProtectedQueryTypeDef):
    pass

AnalysisRuleTypeDef = TypedDict(
    "AnalysisRuleTypeDef",
    {
        "collaborationId": str,
        "type": AnalysisRuleTypeType,
        "name": str,
        "createTime": datetime,
        "updateTime": datetime,
        "policy": AnalysisRulePolicyTypeDef,
    },
)

ConfiguredTableAnalysisRuleTypeDef = TypedDict(
    "ConfiguredTableAnalysisRuleTypeDef",
    {
        "configuredTableId": str,
        "configuredTableArn": str,
        "policy": ConfiguredTableAnalysisRulePolicyTypeDef,
        "type": ConfiguredTableAnalysisRuleTypeType,
        "createTime": datetime,
        "updateTime": datetime,
    },
)

CreateConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "CreateConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
        "analysisRulePolicy": ConfiguredTableAnalysisRulePolicyTypeDef,
    },
)

UpdateConfiguredTableAnalysisRuleInputRequestTypeDef = TypedDict(
    "UpdateConfiguredTableAnalysisRuleInputRequestTypeDef",
    {
        "configuredTableIdentifier": str,
        "analysisRuleType": ConfiguredTableAnalysisRuleTypeType,
        "analysisRulePolicy": ConfiguredTableAnalysisRulePolicyTypeDef,
    },
)

GetProtectedQueryOutputTypeDef = TypedDict(
    "GetProtectedQueryOutputTypeDef",
    {
        "protectedQuery": ProtectedQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartProtectedQueryOutputTypeDef = TypedDict(
    "StartProtectedQueryOutputTypeDef",
    {
        "protectedQuery": ProtectedQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateProtectedQueryOutputTypeDef = TypedDict(
    "UpdateProtectedQueryOutputTypeDef",
    {
        "protectedQuery": ProtectedQueryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaAnalysisRuleOutputTypeDef = TypedDict(
    "GetSchemaAnalysisRuleOutputTypeDef",
    {
        "analysisRule": AnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConfiguredTableAnalysisRuleOutputTypeDef = TypedDict(
    "CreateConfiguredTableAnalysisRuleOutputTypeDef",
    {
        "analysisRule": ConfiguredTableAnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConfiguredTableAnalysisRuleOutputTypeDef = TypedDict(
    "GetConfiguredTableAnalysisRuleOutputTypeDef",
    {
        "analysisRule": ConfiguredTableAnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConfiguredTableAnalysisRuleOutputTypeDef = TypedDict(
    "UpdateConfiguredTableAnalysisRuleOutputTypeDef",
    {
        "analysisRule": ConfiguredTableAnalysisRuleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
