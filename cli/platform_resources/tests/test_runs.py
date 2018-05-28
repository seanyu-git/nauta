#
# INTEL CONFIDENTIAL
# Copyright (c) 2018 Intel Corporation
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and treaty
# provisions. No part of the Material may be used, copied, reproduced, modified,
# published, uploaded, posted, transmitted, distributed, or disclosed in any way
# without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be express
# and approved by Intel in writing.
#

import pytest

from kubernetes.client import CustomObjectsApi

from platform_resources.run_model import Run, RunStatus
from platform_resources.runs import list_runs

TEST_RUNS = [Run(name="exp-mnist-single-node.py-18.05.17-16.05.45-1-tf-training",
                 parameters=['mnist_single_node.py', '--data_dir', '/app'],
                 state=RunStatus.QUEUED,
                 metrics={'accuracy': 52.322},
                 experiment_name="experiment-name-will-be-added-soon",
                 pod_count=1,
                 pod_selector={'matchLabels': {'app': 'tf-training',
                                               'draft': 'exp-mnist-single-node.py-18.05.17-16.05.45-1',
                                               'release': 'exp-mnist-single-node.py-18.05.17-16.05.45-1'}},
                 submitter="mciesiel-dev", creation_timestamp="2018-05-17T14:05:52Z"),
             Run(name="exp-mnist-single-node.py-18.05.17-16.05.56-2-tf-training",
                 parameters=['mnist_single_node.py', '--data_dir', '/app'], state=RunStatus.QUEUED,
                 metrics={'accuracy': 52.322}, experiment_name="experiment-name-will-be-added-soon", pod_count=1,
                 pod_selector={
                     'matchLabels': {'app': 'tf-training', 'draft': 'exp-mnist-single-node.py-18.05.17-16.05.56-2',
                                     'release': 'exp-mnist-single-node.py-18.05.17-16.05.56-2'}},
                 submitter="mciesiel-dev", creation_timestamp="2018-05-17T14:06:03Z")]


@pytest.fixture()
def mock_k8s_api_client(mocker) -> CustomObjectsApi:
    mocker.patch('kubernetes.config.load_kube_config')
    mocker.patch('kubernetes.client.ApiClient')
    custom_objects_api_mocked_class = mocker.patch('kubernetes.client.CustomObjectsApi')
    return custom_objects_api_mocked_class.return_value


def test_list_runs(mock_k8s_api_client):
    mock_k8s_api_client.list_cluster_custom_object.return_value = LIST_RUNS_RESPONSE_RAW
    runs = list_runs()
    assert runs == TEST_RUNS


LIST_RUNS_RESPONSE_RAW = {'apiVersion': 'aipg.intel.com/v1', 'items': [
    {'apiVersion': 'aipg.intel.com/v1', 'kind': 'Run',
     'metadata': {'clusterName': '', 'creationTimestamp': '2018-05-17T14:05:52Z', 'generation': 1,
                  'name': 'exp-mnist-single-node.py-18.05.17-16.05.45-1-tf-training', 'namespace': 'mciesiel-dev',
                  'resourceVersion': '435977',
                  'selfLink': '/apis/aipg.intel.com/v1/namespaces/mciesiel-dev/runs/'
                              'exp-mnist-single-node.py-18.05.17-16.05.45-1-tf-training',
                  'uid': '68af2c7a-59db-11e8-b5db-527100001250'},
     'spec': {'experiment-name': 'experiment-name-will-be-added-soon', 'metrics': {'accuracy': 52.322},
              'name': 'exp-mnist-single-node.py-18.05.17-16.05.45-1-tf-training',
              'parameters': ['mnist_single_node.py', '--data_dir', '/app'], 'pod-count': 1, 'pod-selector': {
             'matchLabels': {'app': 'tf-training', 'draft': 'exp-mnist-single-node.py-18.05.17-16.05.45-1',
                             'release': 'exp-mnist-single-node.py-18.05.17-16.05.45-1'}}, 'state': 'QUEUED'}},
    {'apiVersion': 'aipg.intel.com/v1', 'kind': 'Run',
     'metadata': {'clusterName': '', 'creationTimestamp': '2018-05-17T14:06:03Z', 'generation': 1,
                  'name': 'exp-mnist-single-node.py-18.05.17-16.05.56-2-tf-training', 'namespace': 'mciesiel-dev',
                  'resourceVersion': '436010',
                  'selfLink': '/apis/aipg.intel.com/v1/namespaces/mciesiel-dev/runs/'
                              'exp-mnist-single-node.py-18.05.17-16.05.56-2-tf-training',
                  'uid': '6f13b47c-59db-11e8-b5db-527100001250'},
     'spec': {'experiment-name': 'experiment-name-will-be-added-soon', 'metrics': {'accuracy': 52.322},
              'name': 'exp-mnist-single-node.py-18.05.17-16.05.56-2-tf-training',
              'parameters': ['mnist_single_node.py', '--data_dir', '/app'], 'pod-count': 1, 'pod-selector': {
             'matchLabels': {'app': 'tf-training', 'draft': 'exp-mnist-single-node.py-18.05.17-16.05.56-2',
                             'release': 'exp-mnist-single-node.py-18.05.17-16.05.56-2'}}, 'state': 'QUEUED'}}],
                          'kind': 'RunList', 'metadata': {'continue': '', 'resourceVersion': '436078',
                                                          'selfLink': '/apis/aipg.intel.com/v1/runs'}}