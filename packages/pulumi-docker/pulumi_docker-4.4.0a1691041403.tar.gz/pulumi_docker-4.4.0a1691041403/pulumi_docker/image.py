# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from ._enums import *
from ._inputs import *

__all__ = ['ImageArgs', 'Image']

@pulumi.input_type
class ImageArgs:
    def __init__(__self__, *,
                 image_name: pulumi.Input[str],
                 build: Optional[pulumi.Input['DockerBuildArgs']] = None,
                 registry: Optional[pulumi.Input['RegistryArgs']] = None,
                 skip_push: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Image resource.
        :param pulumi.Input[str] image_name: The image name
        :param pulumi.Input['DockerBuildArgs'] build: The Docker build context
        :param pulumi.Input['RegistryArgs'] registry: The registry to push the image to
        :param pulumi.Input[bool] skip_push: A flag to skip a registry push.
        """
        pulumi.set(__self__, "image_name", image_name)
        if build is not None:
            pulumi.set(__self__, "build", build)
        if registry is not None:
            pulumi.set(__self__, "registry", registry)
        if skip_push is None:
            skip_push = False
        if skip_push is not None:
            pulumi.set(__self__, "skip_push", skip_push)

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> pulumi.Input[str]:
        """
        The image name
        """
        return pulumi.get(self, "image_name")

    @image_name.setter
    def image_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "image_name", value)

    @property
    @pulumi.getter
    def build(self) -> Optional[pulumi.Input['DockerBuildArgs']]:
        """
        The Docker build context
        """
        return pulumi.get(self, "build")

    @build.setter
    def build(self, value: Optional[pulumi.Input['DockerBuildArgs']]):
        pulumi.set(self, "build", value)

    @property
    @pulumi.getter
    def registry(self) -> Optional[pulumi.Input['RegistryArgs']]:
        """
        The registry to push the image to
        """
        return pulumi.get(self, "registry")

    @registry.setter
    def registry(self, value: Optional[pulumi.Input['RegistryArgs']]):
        pulumi.set(self, "registry", value)

    @property
    @pulumi.getter(name="skipPush")
    def skip_push(self) -> Optional[pulumi.Input[bool]]:
        """
        A flag to skip a registry push.
        """
        return pulumi.get(self, "skip_push")

    @skip_push.setter
    def skip_push(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "skip_push", value)


class Image(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 build: Optional[pulumi.Input[pulumi.InputType['DockerBuildArgs']]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 registry: Optional[pulumi.Input[pulumi.InputType['RegistryArgs']]] = None,
                 skip_push: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        `Image` builds a Docker image and pushes it Docker and OCI compatible registries.
        This resource enables running Docker builds as part of a Pulumi deployment.

        Note: This resource does not delete tags, locally or remotely, when destroyed.

        ## Cross-platform builds

        The Image resource supports cross-platform builds when the [Docker engine has cross-platform support enabled via emulators](https://docs.docker.com/build/building/multi-platform/#building-multi-platform-images).
        The Image resource currently supports providing only a single operating system and architecture in the `platform` field, e.g.: `linux/amd64`.
        To enable this support, you may need to install the emulators in the environment running your Pulumi program.

        If you are using Linux, you may be using Docker Engine or Docker Desktop for Linux, depending on how you have installed Docker. The [FAQ for Docker Desktop for Linux](https://docs.docker.com/desktop/faqs/linuxfaqs/#context) describes the differences and how to select which Docker context is in use.

        * For local development using Docker Desktop, this is enabled by default.
        * For systems using Docker Engine, install the QEMU binaries and register them with using the docker image from [github.com/tonistiigi/binfmt](https://github.com/tonistiigi/binfmt):
        * In a GitHub Actions workflow, the [docker/setup-qemu-action](https://github.com/docker/setup-qemu-action) can be used instead by adding this step to your workflow file. Example workflow usage:

        ## Example Usage
        ### A Docker image build
        ```python
        import pulumi
        import pulumi_docker as docker

        demo_image = docker.Image("demo-image",
            build=docker.DockerBuildArgs(
                context=".",
                dockerfile="Dockerfile",
            ),
            image_name="username/image:tag1",
            skip_push=True)
        pulumi.export("imageName", demo_image.image_name)
        ```
        ### Docker image build using caching with AWS Elastic Container Registry
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_docker as docker

        ecr_repository = aws.ecr.Repository("ecr-repository", name="docker-repository")
        auth_token = aws.ecr.get_authorization_token_output(registry_id=ecr_repository.registry_id)
        my_app_image = docker.Image("my-app-image",
            build=docker.DockerBuildArgs(
                args={
                    "BUILDKIT_INLINE_CACHE": "1",
                },
                cache_from=docker.CacheFromArgs(
                    images=[ecr_repository.repository_url.apply(lambda repository_url: f"{repository_url}:latest")],
                ),
                context="app/",
                dockerfile="Dockerfile",
            ),
            image_name=ecr_repository.repository_url.apply(lambda repository_url: f"{repository_url}:latest"),
            registry=docker.RegistryArgs(
                password=pulumi.Output.secret(auth_token.password),
                server=ecr_repository.repository_url,
            ))
        pulumi.export("imageName", my_app_image.image_name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['DockerBuildArgs']] build: The Docker build context
        :param pulumi.Input[str] image_name: The image name
        :param pulumi.Input[pulumi.InputType['RegistryArgs']] registry: The registry to push the image to
        :param pulumi.Input[bool] skip_push: A flag to skip a registry push.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ImageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        `Image` builds a Docker image and pushes it Docker and OCI compatible registries.
        This resource enables running Docker builds as part of a Pulumi deployment.

        Note: This resource does not delete tags, locally or remotely, when destroyed.

        ## Cross-platform builds

        The Image resource supports cross-platform builds when the [Docker engine has cross-platform support enabled via emulators](https://docs.docker.com/build/building/multi-platform/#building-multi-platform-images).
        The Image resource currently supports providing only a single operating system and architecture in the `platform` field, e.g.: `linux/amd64`.
        To enable this support, you may need to install the emulators in the environment running your Pulumi program.

        If you are using Linux, you may be using Docker Engine or Docker Desktop for Linux, depending on how you have installed Docker. The [FAQ for Docker Desktop for Linux](https://docs.docker.com/desktop/faqs/linuxfaqs/#context) describes the differences and how to select which Docker context is in use.

        * For local development using Docker Desktop, this is enabled by default.
        * For systems using Docker Engine, install the QEMU binaries and register them with using the docker image from [github.com/tonistiigi/binfmt](https://github.com/tonistiigi/binfmt):
        * In a GitHub Actions workflow, the [docker/setup-qemu-action](https://github.com/docker/setup-qemu-action) can be used instead by adding this step to your workflow file. Example workflow usage:

        ## Example Usage
        ### A Docker image build
        ```python
        import pulumi
        import pulumi_docker as docker

        demo_image = docker.Image("demo-image",
            build=docker.DockerBuildArgs(
                context=".",
                dockerfile="Dockerfile",
            ),
            image_name="username/image:tag1",
            skip_push=True)
        pulumi.export("imageName", demo_image.image_name)
        ```
        ### Docker image build using caching with AWS Elastic Container Registry
        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_docker as docker

        ecr_repository = aws.ecr.Repository("ecr-repository", name="docker-repository")
        auth_token = aws.ecr.get_authorization_token_output(registry_id=ecr_repository.registry_id)
        my_app_image = docker.Image("my-app-image",
            build=docker.DockerBuildArgs(
                args={
                    "BUILDKIT_INLINE_CACHE": "1",
                },
                cache_from=docker.CacheFromArgs(
                    images=[ecr_repository.repository_url.apply(lambda repository_url: f"{repository_url}:latest")],
                ),
                context="app/",
                dockerfile="Dockerfile",
            ),
            image_name=ecr_repository.repository_url.apply(lambda repository_url: f"{repository_url}:latest"),
            registry=docker.RegistryArgs(
                password=pulumi.Output.secret(auth_token.password),
                server=ecr_repository.repository_url,
            ))
        pulumi.export("imageName", my_app_image.image_name)
        ```

        :param str resource_name: The name of the resource.
        :param ImageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 build: Optional[pulumi.Input[pulumi.InputType['DockerBuildArgs']]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 registry: Optional[pulumi.Input[pulumi.InputType['RegistryArgs']]] = None,
                 skip_push: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ImageArgs.__new__(ImageArgs)

            __props__.__dict__["build"] = build
            if image_name is None and not opts.urn:
                raise TypeError("Missing required property 'image_name'")
            __props__.__dict__["image_name"] = image_name
            __props__.__dict__["registry"] = registry
            if skip_push is None:
                skip_push = False
            __props__.__dict__["skip_push"] = skip_push
            __props__.__dict__["base_image_name"] = None
            __props__.__dict__["context"] = None
            __props__.__dict__["dockerfile"] = None
            __props__.__dict__["registry_server"] = None
            __props__.__dict__["repo_digest"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="docker:image:Image")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Image, __self__).__init__(
            'docker:index/image:Image',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Image':
        """
        Get an existing Image resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ImageArgs.__new__(ImageArgs)

        __props__.__dict__["base_image_name"] = None
        __props__.__dict__["context"] = None
        __props__.__dict__["dockerfile"] = None
        __props__.__dict__["image_name"] = None
        __props__.__dict__["registry_server"] = None
        __props__.__dict__["repo_digest"] = None
        return Image(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="baseImageName")
    def base_image_name(self) -> pulumi.Output[str]:
        """
        The fully qualified image name that was pushed to the registry.
        """
        return pulumi.get(self, "base_image_name")

    @property
    @pulumi.getter
    def context(self) -> pulumi.Output[str]:
        """
        The path to the build context to use.
        """
        return pulumi.get(self, "context")

    @property
    @pulumi.getter
    def dockerfile(self) -> pulumi.Output[str]:
        """
        The location of the Dockerfile relative to the docker build context.
        """
        return pulumi.get(self, "dockerfile")

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> pulumi.Output[str]:
        """
        The fully qualified image name
        """
        return pulumi.get(self, "image_name")

    @property
    @pulumi.getter(name="registryServer")
    def registry_server(self) -> pulumi.Output[str]:
        """
        The name of the registry server hosting the image.
        """
        return pulumi.get(self, "registry_server")

    @property
    @pulumi.getter(name="repoDigest")
    def repo_digest(self) -> pulumi.Output[Optional[str]]:
        """
        The digest of the manifest pushed to the registry, e.g.: repo[:tag]@<algorithm>:<hash>
        """
        return pulumi.get(self, "repo_digest")

