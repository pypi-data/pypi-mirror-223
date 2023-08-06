'''
# `data_launchdarkly_feature_flag_environment`

Refer to the Terraform Registory for docs: [`data_launchdarkly_feature_flag_environment`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataLaunchdarklyFeatureFlagEnvironment(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment launchdarkly_feature_flag_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        env_key: builtins.str,
        flag_id: builtins.str,
        context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentContextTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fallthrough: typing.Optional[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentFallthrough", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        off_variation: typing.Optional[jsii.Number] = None,
        on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentPrerequisites", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment launchdarkly_feature_flag_environment} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_key: The LaunchDarkly environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#env_key DataLaunchdarklyFeatureFlagEnvironment#env_key}
        :param flag_id: The global feature flag's unique id in the format ``<project_key>/<flag_key>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#flag_id DataLaunchdarklyFeatureFlagEnvironment#flag_id}
        :param context_targets: context_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_targets DataLaunchdarklyFeatureFlagEnvironment#context_targets}
        :param fallthrough: fallthrough block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#fallthrough DataLaunchdarklyFeatureFlagEnvironment#fallthrough}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#id DataLaunchdarklyFeatureFlagEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param off_variation: The index of the variation to serve if targeting is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#off_variation DataLaunchdarklyFeatureFlagEnvironment#off_variation}
        :param on: Whether targeting is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#on DataLaunchdarklyFeatureFlagEnvironment#on}
        :param prerequisites: prerequisites block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#prerequisites DataLaunchdarklyFeatureFlagEnvironment#prerequisites}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rules DataLaunchdarklyFeatureFlagEnvironment#rules}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#targets DataLaunchdarklyFeatureFlagEnvironment#targets}
        :param track_events: Whether to send event data back to LaunchDarkly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#track_events DataLaunchdarklyFeatureFlagEnvironment#track_events}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c7201088cc682989cfe4a66f317bf8c78a4e980658850fce9ac9a9e35331b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLaunchdarklyFeatureFlagEnvironmentConfig(
            env_key=env_key,
            flag_id=flag_id,
            context_targets=context_targets,
            fallthrough=fallthrough,
            id=id,
            off_variation=off_variation,
            on=on,
            prerequisites=prerequisites,
            rules=rules,
            targets=targets,
            track_events=track_events,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putContextTargets")
    def put_context_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentContextTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca7717167f7c0b06032b6942c8f4cd2d92696f7026dc4a39b210ad496db9f1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContextTargets", [value]))

    @jsii.member(jsii_name="putFallthrough")
    def put_fallthrough(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        context_kind: typing.Optional[builtins.str] = None,
        rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
        variation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#bucket_by DataLaunchdarklyFeatureFlagEnvironment#bucket_by}
        :param context_kind: The context kind associated with the specified rollout. This argument is only valid if rollout_weights is also specified. If omitted, defaults to 'user' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_kind DataLaunchdarklyFeatureFlagEnvironment#context_kind}
        :param rollout_weights: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rollout_weights DataLaunchdarklyFeatureFlagEnvironment#rollout_weights}.
        :param variation: The integer variation index to serve in case of fallthrough. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        value = DataLaunchdarklyFeatureFlagEnvironmentFallthrough(
            bucket_by=bucket_by,
            context_kind=context_kind,
            rollout_weights=rollout_weights,
            variation=variation,
        )

        return typing.cast(None, jsii.invoke(self, "putFallthrough", [value]))

    @jsii.member(jsii_name="putPrerequisites")
    def put_prerequisites(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentPrerequisites", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f13fba14f338ab38c65e6a04f9a0f4d32d346ed065008ad75742a3add9da6a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrerequisites", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbdb11a4512b3cc628dc3c0dc46fc47ec30f23b0d3b97c472c277866edd87a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putTargets")
    def put_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114dcbd6ec582798fef8c6680fcf3355b1dd2acd270d1a499d8b5caa7b46e7a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargets", [value]))

    @jsii.member(jsii_name="resetContextTargets")
    def reset_context_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextTargets", []))

    @jsii.member(jsii_name="resetFallthrough")
    def reset_fallthrough(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFallthrough", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOffVariation")
    def reset_off_variation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOffVariation", []))

    @jsii.member(jsii_name="resetOn")
    def reset_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOn", []))

    @jsii.member(jsii_name="resetPrerequisites")
    def reset_prerequisites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrerequisites", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="resetTargets")
    def reset_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargets", []))

    @jsii.member(jsii_name="resetTrackEvents")
    def reset_track_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackEvents", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="contextTargets")
    def context_targets(
        self,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList", jsii.get(self, "contextTargets"))

    @builtins.property
    @jsii.member(jsii_name="fallthrough")
    def fallthrough(
        self,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference", jsii.get(self, "fallthrough"))

    @builtins.property
    @jsii.member(jsii_name="prerequisites")
    def prerequisites(
        self,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList", jsii.get(self, "prerequisites"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "DataLaunchdarklyFeatureFlagEnvironmentRulesList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> "DataLaunchdarklyFeatureFlagEnvironmentTargetsList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="contextTargetsInput")
    def context_targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentContextTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentContextTargets"]]], jsii.get(self, "contextTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="envKeyInput")
    def env_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="fallthroughInput")
    def fallthrough_input(
        self,
    ) -> typing.Optional["DataLaunchdarklyFeatureFlagEnvironmentFallthrough"]:
        return typing.cast(typing.Optional["DataLaunchdarklyFeatureFlagEnvironmentFallthrough"], jsii.get(self, "fallthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="flagIdInput")
    def flag_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flagIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="offVariationInput")
    def off_variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "offVariationInput"))

    @builtins.property
    @jsii.member(jsii_name="onInput")
    def on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onInput"))

    @builtins.property
    @jsii.member(jsii_name="prerequisitesInput")
    def prerequisites_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentPrerequisites"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentPrerequisites"]]], jsii.get(self, "prerequisitesInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentTargets"]]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="trackEventsInput")
    def track_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trackEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="envKey")
    def env_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envKey"))

    @env_key.setter
    def env_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48052dd6c7a023dcecce6585b80141ef2bf75e8bbea9ae6bb4c77a27c682b8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envKey", value)

    @builtins.property
    @jsii.member(jsii_name="flagId")
    def flag_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flagId"))

    @flag_id.setter
    def flag_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126d671c6f1e79cde7b6e0da7da9d97f229102e9d719fd234c6359ff50734169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flagId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37431ffbfa1344495d2467f4e57cfddc0fd29de83f198523798d359debefb4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="offVariation")
    def off_variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offVariation"))

    @off_variation.setter
    def off_variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a8e2e258c9a4fe91d359eea1543965b7742bb40a2a44ff5c4435ddf9a9cc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offVariation", value)

    @builtins.property
    @jsii.member(jsii_name="on")
    def on(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "on"))

    @on.setter
    def on(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faacd5f761f2c1470a7757df93e4c71c5bb6c5902526f4e3280805a994604577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "on", value)

    @builtins.property
    @jsii.member(jsii_name="trackEvents")
    def track_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trackEvents"))

    @track_events.setter
    def track_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f58747e70e076692dc55cacd0b32d2e093542e57ce50c45c93fde4ac3fcbb63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackEvents", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "env_key": "envKey",
        "flag_id": "flagId",
        "context_targets": "contextTargets",
        "fallthrough": "fallthrough",
        "id": "id",
        "off_variation": "offVariation",
        "on": "on",
        "prerequisites": "prerequisites",
        "rules": "rules",
        "targets": "targets",
        "track_events": "trackEvents",
    },
)
class DataLaunchdarklyFeatureFlagEnvironmentConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        env_key: builtins.str,
        flag_id: builtins.str,
        context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentContextTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fallthrough: typing.Optional[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentFallthrough", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        off_variation: typing.Optional[jsii.Number] = None,
        on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentPrerequisites", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_key: The LaunchDarkly environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#env_key DataLaunchdarklyFeatureFlagEnvironment#env_key}
        :param flag_id: The global feature flag's unique id in the format ``<project_key>/<flag_key>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#flag_id DataLaunchdarklyFeatureFlagEnvironment#flag_id}
        :param context_targets: context_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_targets DataLaunchdarklyFeatureFlagEnvironment#context_targets}
        :param fallthrough: fallthrough block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#fallthrough DataLaunchdarklyFeatureFlagEnvironment#fallthrough}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#id DataLaunchdarklyFeatureFlagEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param off_variation: The index of the variation to serve if targeting is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#off_variation DataLaunchdarklyFeatureFlagEnvironment#off_variation}
        :param on: Whether targeting is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#on DataLaunchdarklyFeatureFlagEnvironment#on}
        :param prerequisites: prerequisites block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#prerequisites DataLaunchdarklyFeatureFlagEnvironment#prerequisites}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rules DataLaunchdarklyFeatureFlagEnvironment#rules}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#targets DataLaunchdarklyFeatureFlagEnvironment#targets}
        :param track_events: Whether to send event data back to LaunchDarkly. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#track_events DataLaunchdarklyFeatureFlagEnvironment#track_events}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fallthrough, dict):
            fallthrough = DataLaunchdarklyFeatureFlagEnvironmentFallthrough(**fallthrough)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3887b8a55bec50ce0052798f0dc17b208c0f50312a4ba4a1a14d0afb5a2ac31c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument env_key", value=env_key, expected_type=type_hints["env_key"])
            check_type(argname="argument flag_id", value=flag_id, expected_type=type_hints["flag_id"])
            check_type(argname="argument context_targets", value=context_targets, expected_type=type_hints["context_targets"])
            check_type(argname="argument fallthrough", value=fallthrough, expected_type=type_hints["fallthrough"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument off_variation", value=off_variation, expected_type=type_hints["off_variation"])
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
            check_type(argname="argument prerequisites", value=prerequisites, expected_type=type_hints["prerequisites"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument track_events", value=track_events, expected_type=type_hints["track_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env_key": env_key,
            "flag_id": flag_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if context_targets is not None:
            self._values["context_targets"] = context_targets
        if fallthrough is not None:
            self._values["fallthrough"] = fallthrough
        if id is not None:
            self._values["id"] = id
        if off_variation is not None:
            self._values["off_variation"] = off_variation
        if on is not None:
            self._values["on"] = on
        if prerequisites is not None:
            self._values["prerequisites"] = prerequisites
        if rules is not None:
            self._values["rules"] = rules
        if targets is not None:
            self._values["targets"] = targets
        if track_events is not None:
            self._values["track_events"] = track_events

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def env_key(self) -> builtins.str:
        '''The LaunchDarkly environment key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#env_key DataLaunchdarklyFeatureFlagEnvironment#env_key}
        '''
        result = self._values.get("env_key")
        assert result is not None, "Required property 'env_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flag_id(self) -> builtins.str:
        '''The global feature flag's unique id in the format ``<project_key>/<flag_key>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#flag_id DataLaunchdarklyFeatureFlagEnvironment#flag_id}
        '''
        result = self._values.get("flag_id")
        assert result is not None, "Required property 'flag_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def context_targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentContextTargets"]]]:
        '''context_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_targets DataLaunchdarklyFeatureFlagEnvironment#context_targets}
        '''
        result = self._values.get("context_targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentContextTargets"]]], result)

    @builtins.property
    def fallthrough(
        self,
    ) -> typing.Optional["DataLaunchdarklyFeatureFlagEnvironmentFallthrough"]:
        '''fallthrough block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#fallthrough DataLaunchdarklyFeatureFlagEnvironment#fallthrough}
        '''
        result = self._values.get("fallthrough")
        return typing.cast(typing.Optional["DataLaunchdarklyFeatureFlagEnvironmentFallthrough"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#id DataLaunchdarklyFeatureFlagEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def off_variation(self) -> typing.Optional[jsii.Number]:
        '''The index of the variation to serve if targeting is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#off_variation DataLaunchdarklyFeatureFlagEnvironment#off_variation}
        '''
        result = self._values.get("off_variation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether targeting is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#on DataLaunchdarklyFeatureFlagEnvironment#on}
        '''
        result = self._values.get("on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prerequisites(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentPrerequisites"]]]:
        '''prerequisites block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#prerequisites DataLaunchdarklyFeatureFlagEnvironment#prerequisites}
        '''
        result = self._values.get("prerequisites")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentPrerequisites"]]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rules DataLaunchdarklyFeatureFlagEnvironment#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentRules"]]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentTargets"]]]:
        '''targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#targets DataLaunchdarklyFeatureFlagEnvironment#targets}
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentTargets"]]], result)

    @builtins.property
    def track_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to send event data back to LaunchDarkly.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#track_events DataLaunchdarklyFeatureFlagEnvironment#track_events}
        '''
        result = self._values.get("track_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentContextTargets",
    jsii_struct_bases=[],
    name_mapping={
        "context_kind": "contextKind",
        "values": "values",
        "variation": "variation",
    },
)
class DataLaunchdarklyFeatureFlagEnvironmentContextTargets:
    def __init__(
        self,
        *,
        context_kind: builtins.str,
        values: typing.Sequence[builtins.str],
        variation: jsii.Number,
    ) -> None:
        '''
        :param context_kind: The context kind on which the flag should target in this environment. If the context_kind has not been previously specified at the project level, it will be automatically created on the project. User targets should be specified as targets attribute blocks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_kind DataLaunchdarklyFeatureFlagEnvironment#context_kind}
        :param values: List of user strings to target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#values DataLaunchdarklyFeatureFlagEnvironment#values}
        :param variation: Index of the variation to serve if a user_target is matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bd5d9c2e613d9db4ae3ca3493dfbc81dab0115207eff4272d188b6b6a50829)
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context_kind": context_kind,
            "values": values,
            "variation": variation,
        }

    @builtins.property
    def context_kind(self) -> builtins.str:
        '''The context kind on which the flag should target in this environment.

        If the context_kind has not been previously specified at the project level, it will be automatically created on the project. User targets should be specified as targets attribute blocks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_kind DataLaunchdarklyFeatureFlagEnvironment#context_kind}
        '''
        result = self._values.get("context_kind")
        assert result is not None, "Required property 'context_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of user strings to target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#values DataLaunchdarklyFeatureFlagEnvironment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def variation(self) -> jsii.Number:
        '''Index of the variation to serve if a user_target is matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        assert result is not None, "Required property 'variation' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentContextTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c861f85a336823e80a111eef51d967f3dc260ee12f6ceb139a6774c1b67bb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96e15de5a7e338cffd5f55069f05f939e9be8c9746a3ec2ca49ccc24974be04)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d31c4c8d97cde5aedd817fe5dbae1d13d56b76121dedb2872471f292e9967c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6652b7937d676f69b4c17dbb1ee6f3bc0828e41428e2aaa246f2de48a90340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c7771d66b8cbbd7375b2c3309eb3201d96df03b6b2eed59e62f1b9594bab9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentContextTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentContextTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentContextTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a925b252e840a3d7dc0086c3fe00ea74d22a7f6f65b40403ee6b38f6e7c7207f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce5546370a9059518904401e231c12a1170cc38c130f333f53bdfc1420c0cace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0704419db50f06d6922dc788415c7db73c4143ff9b23d14efb531c18090f554b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ca0c762eec4c05550a32340732948e8e68721d2e06437316d7097ccc977adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27570c4c2b7019ede7922aae756a0cf31a66627ca16f3f3abe4cf277cedd7dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentContextTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentContextTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentContextTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc8b87db97e573193c6c5d83a5210998f1a0779cef76678e95d50d43e5e9273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentFallthrough",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_by": "bucketBy",
        "context_kind": "contextKind",
        "rollout_weights": "rolloutWeights",
        "variation": "variation",
    },
)
class DataLaunchdarklyFeatureFlagEnvironmentFallthrough:
    def __init__(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        context_kind: typing.Optional[builtins.str] = None,
        rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
        variation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#bucket_by DataLaunchdarklyFeatureFlagEnvironment#bucket_by}
        :param context_kind: The context kind associated with the specified rollout. This argument is only valid if rollout_weights is also specified. If omitted, defaults to 'user' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_kind DataLaunchdarklyFeatureFlagEnvironment#context_kind}
        :param rollout_weights: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rollout_weights DataLaunchdarklyFeatureFlagEnvironment#rollout_weights}.
        :param variation: The integer variation index to serve in case of fallthrough. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd35911240626a0307f449f70c6ec7d35e046146500f2b7c3e36879d33ef46d)
            check_type(argname="argument bucket_by", value=bucket_by, expected_type=type_hints["bucket_by"])
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument rollout_weights", value=rollout_weights, expected_type=type_hints["rollout_weights"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_by is not None:
            self._values["bucket_by"] = bucket_by
        if context_kind is not None:
            self._values["context_kind"] = context_kind
        if rollout_weights is not None:
            self._values["rollout_weights"] = rollout_weights
        if variation is not None:
            self._values["variation"] = variation

    @builtins.property
    def bucket_by(self) -> typing.Optional[builtins.str]:
        '''Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#bucket_by DataLaunchdarklyFeatureFlagEnvironment#bucket_by}
        '''
        result = self._values.get("bucket_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with the specified rollout.

        This argument is only valid if rollout_weights is also specified. If omitted, defaults to 'user'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_kind DataLaunchdarklyFeatureFlagEnvironment#context_kind}
        '''
        result = self._values.get("context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollout_weights(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rollout_weights DataLaunchdarklyFeatureFlagEnvironment#rollout_weights}.'''
        result = self._values.get("rollout_weights")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def variation(self) -> typing.Optional[jsii.Number]:
        '''The integer variation index to serve in case of fallthrough.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentFallthrough(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a4f0fbb1b5671a2a896f5d94f94956c2c9a5bd6014dec31f958f1c75cf881d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketBy")
    def reset_bucket_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketBy", []))

    @jsii.member(jsii_name="resetContextKind")
    def reset_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextKind", []))

    @jsii.member(jsii_name="resetRolloutWeights")
    def reset_rollout_weights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutWeights", []))

    @jsii.member(jsii_name="resetVariation")
    def reset_variation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariation", []))

    @builtins.property
    @jsii.member(jsii_name="bucketByInput")
    def bucket_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketByInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutWeightsInput")
    def rollout_weights_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "rolloutWeightsInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @bucket_by.setter
    def bucket_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b17de1780ead3ed22b65c7edc013aca7fb18f84533468c6bf2120f22b123377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketBy", value)

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b090fc5efa2826247785723762ccd11dcfd120e50460f2973c9e6d018f37582c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value)

    @builtins.property
    @jsii.member(jsii_name="rolloutWeights")
    def rollout_weights(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "rolloutWeights"))

    @rollout_weights.setter
    def rollout_weights(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d513e318ecd2fb979346224194d6711735d5986101604756b6e202adac195b7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutWeights", value)

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cddd12f60ed68a67b9169930370d388643a9885d95d5c3fd3895b4dc475b7a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fb75d33b68925215bf849cd7f727caf53de05a1f20217892c8b94bd23e53ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentPrerequisites",
    jsii_struct_bases=[],
    name_mapping={"flag_key": "flagKey", "variation": "variation"},
)
class DataLaunchdarklyFeatureFlagEnvironmentPrerequisites:
    def __init__(self, *, flag_key: builtins.str, variation: jsii.Number) -> None:
        '''
        :param flag_key: The prerequisite feature flag's key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#flag_key DataLaunchdarklyFeatureFlagEnvironment#flag_key}
        :param variation: The index of the prerequisite feature flag's variation to target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c67bd97fe0637405ab67046c763cd52428047d5bb6d1fd751672379fd4161e02)
            check_type(argname="argument flag_key", value=flag_key, expected_type=type_hints["flag_key"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flag_key": flag_key,
            "variation": variation,
        }

    @builtins.property
    def flag_key(self) -> builtins.str:
        '''The prerequisite feature flag's key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#flag_key DataLaunchdarklyFeatureFlagEnvironment#flag_key}
        '''
        result = self._values.get("flag_key")
        assert result is not None, "Required property 'flag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def variation(self) -> jsii.Number:
        '''The index of the prerequisite feature flag's variation to target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        assert result is not None, "Required property 'variation' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentPrerequisites(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924162720c08538d0a2a4f14a62324b405effc3c81735ad9cea5fb82bf5c0805)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c31e50dd4fdb761d0e5490128dad96dfe468ffe6a6d5d4ccf8a6abe9257f41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e93255de41cebe537b062c1b0a2372a4e349c879121f3b1bec1e3386b2d16a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc85e480215ef6bcda306cccd212af9ff3e33b322cf085b265acf1ddbf2ecbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7cfc261603b766e25969552c5d75ceabc86da32aee6921783c4667eefe83ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697b7970f5a34e409116baf3cb2e05575361e81b42f190befd03d940855d38b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f4843b547c4d95531c1f74c9b671eae102eb6ca7e0f6442399fb15882fb3d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="flagKeyInput")
    def flag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="flagKey")
    def flag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flagKey"))

    @flag_key.setter
    def flag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39e592c6a9ae3f383a8de93972a4d19381bd5f906da59fab3af593df20a7652b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flagKey", value)

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3615e89705ad511918cfb6c9496219c6a8e40207aa72abb9f7ab73fd673262b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28139a67eeb753d3f28f90b45aec635af3eeef8a7c05cc76b1f2f37c6031eec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_by": "bucketBy",
        "clauses": "clauses",
        "description": "description",
        "rollout_weights": "rolloutWeights",
        "variation": "variation",
    },
)
class DataLaunchdarklyFeatureFlagEnvironmentRules:
    def __init__(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataLaunchdarklyFeatureFlagEnvironmentRulesClauses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
        variation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#bucket_by DataLaunchdarklyFeatureFlagEnvironment#bucket_by}
        :param clauses: clauses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#clauses DataLaunchdarklyFeatureFlagEnvironment#clauses}
        :param description: A human-readable description of the targeting rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#description DataLaunchdarklyFeatureFlagEnvironment#description}
        :param rollout_weights: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rollout_weights DataLaunchdarklyFeatureFlagEnvironment#rollout_weights}.
        :param variation: The integer variation index to serve if the rule clauses evaluate to true. This argument is only valid if clauses are also specified Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707b0657af96d6231b89013d858f53a155af294cc4d7dd98b453c24a68e2344a)
            check_type(argname="argument bucket_by", value=bucket_by, expected_type=type_hints["bucket_by"])
            check_type(argname="argument clauses", value=clauses, expected_type=type_hints["clauses"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rollout_weights", value=rollout_weights, expected_type=type_hints["rollout_weights"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_by is not None:
            self._values["bucket_by"] = bucket_by
        if clauses is not None:
            self._values["clauses"] = clauses
        if description is not None:
            self._values["description"] = description
        if rollout_weights is not None:
            self._values["rollout_weights"] = rollout_weights
        if variation is not None:
            self._values["variation"] = variation

    @builtins.property
    def bucket_by(self) -> typing.Optional[builtins.str]:
        '''Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#bucket_by DataLaunchdarklyFeatureFlagEnvironment#bucket_by}
        '''
        result = self._values.get("bucket_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clauses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentRulesClauses"]]]:
        '''clauses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#clauses DataLaunchdarklyFeatureFlagEnvironment#clauses}
        '''
        result = self._values.get("clauses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataLaunchdarklyFeatureFlagEnvironmentRulesClauses"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the targeting rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#description DataLaunchdarklyFeatureFlagEnvironment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollout_weights(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#rollout_weights DataLaunchdarklyFeatureFlagEnvironment#rollout_weights}.'''
        result = self._values.get("rollout_weights")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def variation(self) -> typing.Optional[jsii.Number]:
        '''The integer variation index to serve if the rule clauses evaluate to true.

        This argument is only valid if clauses are also specified

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesClauses",
    jsii_struct_bases=[],
    name_mapping={
        "attribute": "attribute",
        "op": "op",
        "values": "values",
        "context_kind": "contextKind",
        "negate": "negate",
        "value_type": "valueType",
    },
)
class DataLaunchdarklyFeatureFlagEnvironmentRulesClauses:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        op: builtins.str,
        values: typing.Sequence[builtins.str],
        context_kind: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        value_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute: The user attribute to operate on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#attribute DataLaunchdarklyFeatureFlagEnvironment#attribute}
        :param op: The operator associated with the rule clause. Available options are in, endsWith, startsWith, matches, contains, lessThan, lessThanOrEqual, greaterThanOrEqual, before, after, segmentMatch, semVerEqual, semVerLessThan, and semVerGreaterThan Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#op DataLaunchdarklyFeatureFlagEnvironment#op}
        :param values: The list of values associated with the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#values DataLaunchdarklyFeatureFlagEnvironment#values}
        :param context_kind: The context kind associated with this rule clause. If omitted, defaults to user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_kind DataLaunchdarklyFeatureFlagEnvironment#context_kind}
        :param negate: Whether to negate the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#negate DataLaunchdarklyFeatureFlagEnvironment#negate}
        :param value_type: The type for each of the clause's values. Available types are boolean, string, and number. If omitted, value_type defaults to string Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#value_type DataLaunchdarklyFeatureFlagEnvironment#value_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9c6da1ea595f6b5beb74fd493993178a3f9066a7b4ae13cd29029ee7b53e01)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument op", value=op, expected_type=type_hints["op"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute": attribute,
            "op": op,
            "values": values,
        }
        if context_kind is not None:
            self._values["context_kind"] = context_kind
        if negate is not None:
            self._values["negate"] = negate
        if value_type is not None:
            self._values["value_type"] = value_type

    @builtins.property
    def attribute(self) -> builtins.str:
        '''The user attribute to operate on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#attribute DataLaunchdarklyFeatureFlagEnvironment#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def op(self) -> builtins.str:
        '''The operator associated with the rule clause.

        Available options are in, endsWith, startsWith, matches, contains, lessThan, lessThanOrEqual, greaterThanOrEqual, before, after, segmentMatch, semVerEqual, semVerLessThan, and semVerGreaterThan

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#op DataLaunchdarklyFeatureFlagEnvironment#op}
        '''
        result = self._values.get("op")
        assert result is not None, "Required property 'op' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The list of values associated with the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#values DataLaunchdarklyFeatureFlagEnvironment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with this rule clause. If omitted, defaults to user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#context_kind DataLaunchdarklyFeatureFlagEnvironment#context_kind}
        '''
        result = self._values.get("context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to negate the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#negate DataLaunchdarklyFeatureFlagEnvironment#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''The type for each of the clause's values.

        Available types are boolean, string, and number. If omitted, value_type defaults to string

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#value_type DataLaunchdarklyFeatureFlagEnvironment#value_type}
        '''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentRulesClauses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77d4ea8da9059368daf4cba66cf1e1eac50e7759f7d2476b901988f5827a317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56f48f0390df4691fd02dc191b08847f9ccb4a2a8a092d68057ee5637115a13)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d050aa412d0f4bd721f8b5c5648117e5094e5a1a627b8519b1944f9904fae9eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779226076cba08212cce2c9167e237ef25068487bf21107382d298298e0e0858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c183342773b034d5f74c173910e26f3f7f3c18316909c226cc2661cff781b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc95f15245d11e5230593ba19e5a04848315c4dd0bdee90a6190b685001ac069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848108790c477e871c079f6d89d95b98f539c810e26dbec170b6c15842d8bf11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContextKind")
    def reset_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextKind", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @jsii.member(jsii_name="resetValueType")
    def reset_value_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueType", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="opInput")
    def op_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="valueTypeInput")
    def value_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e2cf9d68b4c7789262228b676ee845d310dd548bf6ab8762c5b4d157502b7b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value)

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0cbfb3148f102ddfc03db2fa077e5c17e667546ffc5ab690ae30713805e5a18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value)

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3164c3c44288765195de1cf65eee4a9befdc8a45e6e4a8ba9df963a13e5f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value)

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @op.setter
    def op(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a9caf36f2c457da698fbc2c1063037e7c2fe121b0b8d2cfbd6dc9bb34ee7f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "op", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c14e58232b652eaf01859ac76ae4c3ec91f029dd30059540cbac64b37454d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3b88ec24585cf1d1038cd301b3623cb8ce41bc25f1528cf41e68846f3e30f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029bca670f80ae9e248a5717fa20e40ef161e132cb41eb9f84ec95d9200c9a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklyFeatureFlagEnvironmentRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13bd484e01f5c8cc11cfc327ec5c7de3953233568cfee096a88972662169e3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c6feccf14873f0fe814689f37e8806c6b854af4795d019a04520889c49e3c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690c441fd37e756e7b7e851912643e27cfc96766883d725f5150a01ed165106c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece46b7986a13cdb4fbe87777a2dc631d54f0bcc14f041d24dfd1149e33eed79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd89e88c0ba9f9f1a4f1b1a866dbea199118796b580894a63f9f23729491423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06934fa1b8e7b9540169b35fa9d768dac19ed233605055770d16dbd9f675bee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ef788ed59cec2a828bf22949d89eb8caa2c51d399f5823838affebb2045b6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putClauses")
    def put_clauses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f87bd76c8c77d1d65f020b0fb462f57e2ed9cec7ff0e7b6baa2d152a54469e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClauses", [value]))

    @jsii.member(jsii_name="resetBucketBy")
    def reset_bucket_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketBy", []))

    @jsii.member(jsii_name="resetClauses")
    def reset_clauses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClauses", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetRolloutWeights")
    def reset_rollout_weights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutWeights", []))

    @jsii.member(jsii_name="resetVariation")
    def reset_variation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariation", []))

    @builtins.property
    @jsii.member(jsii_name="clauses")
    def clauses(self) -> DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList:
        return typing.cast(DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList, jsii.get(self, "clauses"))

    @builtins.property
    @jsii.member(jsii_name="bucketByInput")
    def bucket_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketByInput"))

    @builtins.property
    @jsii.member(jsii_name="clausesInput")
    def clauses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]]], jsii.get(self, "clausesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutWeightsInput")
    def rollout_weights_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "rolloutWeightsInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @bucket_by.setter
    def bucket_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806946c5b6cb7e274245e74e4126c6e339f168d569e930728e7077f5993cc35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketBy", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dacc1fd4a00d872bc9deac2622e2d0d215449db1dafe9f2ff0069b66dbca344f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="rolloutWeights")
    def rollout_weights(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "rolloutWeights"))

    @rollout_weights.setter
    def rollout_weights(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f836bf379563a0ba16b0a21f8f4c83af09a7babcb885934b915ba0c3a25ee3c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutWeights", value)

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b67f3c5019880020af589916f4dfc6b6eb21dd9698bd6494502c16af5f6f4adf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40a846e7e502ae738a10a6d7d2c5c218428d37d0404a08f5104374f088d1597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentTargets",
    jsii_struct_bases=[],
    name_mapping={"values": "values", "variation": "variation"},
)
class DataLaunchdarklyFeatureFlagEnvironmentTargets:
    def __init__(
        self,
        *,
        values: typing.Sequence[builtins.str],
        variation: jsii.Number,
    ) -> None:
        '''
        :param values: List of user strings to target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#values DataLaunchdarklyFeatureFlagEnvironment#values}
        :param variation: Index of the variation to serve if a user_target is matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aba7a0b86e349809185aeca650c0e7f1023822ec9638134c6bb285922e641a7)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "values": values,
            "variation": variation,
        }

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of user strings to target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#values DataLaunchdarklyFeatureFlagEnvironment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def variation(self) -> jsii.Number:
        '''Index of the variation to serve if a user_target is matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.13.4/docs/data-sources/feature_flag_environment#variation DataLaunchdarklyFeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        assert result is not None, "Required property 'variation' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentTargetsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e12d96e69c7e28805563915acec711644a2652c00d293a0a6cbbaf6f96988f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5384d99e6711f0a32b3e6900d6217aa69a29cce4b9fad93bd28faf8880bc6bde)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c751e7e65653992eed5501fdafb8c6b916c6632c0c0a7e353dea31a2886855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a64387f46224e1668fb086319ce8aaf7a675ed58e16f5a5d1df25ca898b1f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4896044257875b27c4d9d992cd34b9dd8a210f02ca0a32f38ab80265837b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbc60ece1e5dbdc0aac5ce1527c0c1641eb63551931a06737f8085c2b163d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5016e2702df0d87756c5095f55d98c02bb93e52dc2b0558fc6400e0fad2af40f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c22ceb91cefcc03ff8957b9f025fe6946ad7b2bbffd31c35c95e724719be6f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4392ae99db7cb4ebfe17d48008be36a4bda5ed4cea8938b07d26ebd9cbb10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e8c92abd94efcff6462039bef5951a5a26d3a7c43f3b20db38becaeba8559c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataLaunchdarklyFeatureFlagEnvironment",
    "DataLaunchdarklyFeatureFlagEnvironmentConfig",
    "DataLaunchdarklyFeatureFlagEnvironmentContextTargets",
    "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList",
    "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentFallthrough",
    "DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentPrerequisites",
    "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList",
    "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentRules",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesClauses",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesList",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentTargets",
    "DataLaunchdarklyFeatureFlagEnvironmentTargetsList",
    "DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference",
]

publication.publish()

def _typecheckingstub__90c7201088cc682989cfe4a66f317bf8c78a4e980658850fce9ac9a9e35331b6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    env_key: builtins.str,
    flag_id: builtins.str,
    context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentContextTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fallthrough: typing.Optional[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentFallthrough, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    off_variation: typing.Optional[jsii.Number] = None,
    on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca7717167f7c0b06032b6942c8f4cd2d92696f7026dc4a39b210ad496db9f1c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentContextTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13fba14f338ab38c65e6a04f9a0f4d32d346ed065008ad75742a3add9da6a3e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbdb11a4512b3cc628dc3c0dc46fc47ec30f23b0d3b97c472c277866edd87a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114dcbd6ec582798fef8c6680fcf3355b1dd2acd270d1a499d8b5caa7b46e7a0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48052dd6c7a023dcecce6585b80141ef2bf75e8bbea9ae6bb4c77a27c682b8c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126d671c6f1e79cde7b6e0da7da9d97f229102e9d719fd234c6359ff50734169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37431ffbfa1344495d2467f4e57cfddc0fd29de83f198523798d359debefb4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a8e2e258c9a4fe91d359eea1543965b7742bb40a2a44ff5c4435ddf9a9cc6b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faacd5f761f2c1470a7757df93e4c71c5bb6c5902526f4e3280805a994604577(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f58747e70e076692dc55cacd0b32d2e093542e57ce50c45c93fde4ac3fcbb63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3887b8a55bec50ce0052798f0dc17b208c0f50312a4ba4a1a14d0afb5a2ac31c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_key: builtins.str,
    flag_id: builtins.str,
    context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentContextTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fallthrough: typing.Optional[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentFallthrough, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    off_variation: typing.Optional[jsii.Number] = None,
    on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bd5d9c2e613d9db4ae3ca3493dfbc81dab0115207eff4272d188b6b6a50829(
    *,
    context_kind: builtins.str,
    values: typing.Sequence[builtins.str],
    variation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c861f85a336823e80a111eef51d967f3dc260ee12f6ceb139a6774c1b67bb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96e15de5a7e338cffd5f55069f05f939e9be8c9746a3ec2ca49ccc24974be04(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d31c4c8d97cde5aedd817fe5dbae1d13d56b76121dedb2872471f292e9967c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6652b7937d676f69b4c17dbb1ee6f3bc0828e41428e2aaa246f2de48a90340(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c7771d66b8cbbd7375b2c3309eb3201d96df03b6b2eed59e62f1b9594bab9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a925b252e840a3d7dc0086c3fe00ea74d22a7f6f65b40403ee6b38f6e7c7207f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentContextTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5546370a9059518904401e231c12a1170cc38c130f333f53bdfc1420c0cace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0704419db50f06d6922dc788415c7db73c4143ff9b23d14efb531c18090f554b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ca0c762eec4c05550a32340732948e8e68721d2e06437316d7097ccc977adc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27570c4c2b7019ede7922aae756a0cf31a66627ca16f3f3abe4cf277cedd7dcc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc8b87db97e573193c6c5d83a5210998f1a0779cef76678e95d50d43e5e9273(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentContextTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd35911240626a0307f449f70c6ec7d35e046146500f2b7c3e36879d33ef46d(
    *,
    bucket_by: typing.Optional[builtins.str] = None,
    context_kind: typing.Optional[builtins.str] = None,
    rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
    variation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a4f0fbb1b5671a2a896f5d94f94956c2c9a5bd6014dec31f958f1c75cf881d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b17de1780ead3ed22b65c7edc013aca7fb18f84533468c6bf2120f22b123377(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b090fc5efa2826247785723762ccd11dcfd120e50460f2973c9e6d018f37582c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d513e318ecd2fb979346224194d6711735d5986101604756b6e202adac195b7b(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cddd12f60ed68a67b9169930370d388643a9885d95d5c3fd3895b4dc475b7a7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fb75d33b68925215bf849cd7f727caf53de05a1f20217892c8b94bd23e53ee(
    value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67bd97fe0637405ab67046c763cd52428047d5bb6d1fd751672379fd4161e02(
    *,
    flag_key: builtins.str,
    variation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924162720c08538d0a2a4f14a62324b405effc3c81735ad9cea5fb82bf5c0805(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c31e50dd4fdb761d0e5490128dad96dfe468ffe6a6d5d4ccf8a6abe9257f41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e93255de41cebe537b062c1b0a2372a4e349c879121f3b1bec1e3386b2d16a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc85e480215ef6bcda306cccd212af9ff3e33b322cf085b265acf1ddbf2ecbb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7cfc261603b766e25969552c5d75ceabc86da32aee6921783c4667eefe83ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697b7970f5a34e409116baf3cb2e05575361e81b42f190befd03d940855d38b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f4843b547c4d95531c1f74c9b671eae102eb6ca7e0f6442399fb15882fb3d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e592c6a9ae3f383a8de93972a4d19381bd5f906da59fab3af593df20a7652b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3615e89705ad511918cfb6c9496219c6a8e40207aa72abb9f7ab73fd673262b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28139a67eeb753d3f28f90b45aec635af3eeef8a7c05cc76b1f2f37c6031eec0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707b0657af96d6231b89013d858f53a155af294cc4d7dd98b453c24a68e2344a(
    *,
    bucket_by: typing.Optional[builtins.str] = None,
    clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
    variation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9c6da1ea595f6b5beb74fd493993178a3f9066a7b4ae13cd29029ee7b53e01(
    *,
    attribute: builtins.str,
    op: builtins.str,
    values: typing.Sequence[builtins.str],
    context_kind: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77d4ea8da9059368daf4cba66cf1e1eac50e7759f7d2476b901988f5827a317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56f48f0390df4691fd02dc191b08847f9ccb4a2a8a092d68057ee5637115a13(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d050aa412d0f4bd721f8b5c5648117e5094e5a1a627b8519b1944f9904fae9eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779226076cba08212cce2c9167e237ef25068487bf21107382d298298e0e0858(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c183342773b034d5f74c173910e26f3f7f3c18316909c226cc2661cff781b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc95f15245d11e5230593ba19e5a04848315c4dd0bdee90a6190b685001ac069(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848108790c477e871c079f6d89d95b98f539c810e26dbec170b6c15842d8bf11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e2cf9d68b4c7789262228b676ee845d310dd548bf6ab8762c5b4d157502b7b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cbfb3148f102ddfc03db2fa077e5c17e667546ffc5ab690ae30713805e5a18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3164c3c44288765195de1cf65eee4a9befdc8a45e6e4a8ba9df963a13e5f1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a9caf36f2c457da698fbc2c1063037e7c2fe121b0b8d2cfbd6dc9bb34ee7f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c14e58232b652eaf01859ac76ae4c3ec91f029dd30059540cbac64b37454d52(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3b88ec24585cf1d1038cd301b3623cb8ce41bc25f1528cf41e68846f3e30f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029bca670f80ae9e248a5717fa20e40ef161e132cb41eb9f84ec95d9200c9a16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13bd484e01f5c8cc11cfc327ec5c7de3953233568cfee096a88972662169e3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c6feccf14873f0fe814689f37e8806c6b854af4795d019a04520889c49e3c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690c441fd37e756e7b7e851912643e27cfc96766883d725f5150a01ed165106c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece46b7986a13cdb4fbe87777a2dc631d54f0bcc14f041d24dfd1149e33eed79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd89e88c0ba9f9f1a4f1b1a866dbea199118796b580894a63f9f23729491423(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06934fa1b8e7b9540169b35fa9d768dac19ed233605055770d16dbd9f675bee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ef788ed59cec2a828bf22949d89eb8caa2c51d399f5823838affebb2045b6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f87bd76c8c77d1d65f020b0fb462f57e2ed9cec7ff0e7b6baa2d152a54469e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806946c5b6cb7e274245e74e4126c6e339f168d569e930728e7077f5993cc35a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dacc1fd4a00d872bc9deac2622e2d0d215449db1dafe9f2ff0069b66dbca344f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f836bf379563a0ba16b0a21f8f4c83af09a7babcb885934b915ba0c3a25ee3c8(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67f3c5019880020af589916f4dfc6b6eb21dd9698bd6494502c16af5f6f4adf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40a846e7e502ae738a10a6d7d2c5c218428d37d0404a08f5104374f088d1597(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aba7a0b86e349809185aeca650c0e7f1023822ec9638134c6bb285922e641a7(
    *,
    values: typing.Sequence[builtins.str],
    variation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e12d96e69c7e28805563915acec711644a2652c00d293a0a6cbbaf6f96988f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5384d99e6711f0a32b3e6900d6217aa69a29cce4b9fad93bd28faf8880bc6bde(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c751e7e65653992eed5501fdafb8c6b916c6632c0c0a7e353dea31a2886855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a64387f46224e1668fb086319ce8aaf7a675ed58e16f5a5d1df25ca898b1f71(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4896044257875b27c4d9d992cd34b9dd8a210f02ca0a32f38ab80265837b25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbc60ece1e5dbdc0aac5ce1527c0c1641eb63551931a06737f8085c2b163d76(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataLaunchdarklyFeatureFlagEnvironmentTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5016e2702df0d87756c5095f55d98c02bb93e52dc2b0558fc6400e0fad2af40f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c22ceb91cefcc03ff8957b9f025fe6946ad7b2bbffd31c35c95e724719be6f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4392ae99db7cb4ebfe17d48008be36a4bda5ed4cea8938b07d26ebd9cbb10c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e8c92abd94efcff6462039bef5951a5a26d3a7c43f3b20db38becaeba8559c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataLaunchdarklyFeatureFlagEnvironmentTargets]],
) -> None:
    """Type checking stubs"""
    pass
