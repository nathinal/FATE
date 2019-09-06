#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from federatedml.linear_regression.base_linear_regression import BaseLinearRegression
from federatedml.util import consts
from federatedml.util.transfer_variable.hetero_linr_transfer_variable import HeteroLinRTransferVariable

class HeteroLinRBase(BaseLinearRegression):
    def __init__(self):
        super().__init__()
        self.model_name = 'HeteroLinearRegression'
        self.model_param_name = 'HeteroLinearRegressionParam'
        self.model_meta_name = 'HeteroLinearRegressionMeta'
        self.mode = consts.HETERO
        self.aggregator = None
        self.cipher = None
        self.batch_generator = None
        self.loss_computer = None
        self.gradient_procedure = None
        self.converge_procedure = None

    def _init_model(self, params):
        super(HeteroLinRBase, self)._init_model(params)
        self.transfer_variable = HeteroLinRTransferVariable()
        self.aggregator.register_aggregator(self.transfer_variable)
        self.cipher.register_paillier_cipher(self.transfer_variable)
        self.converge_procedure.register_convergence(self.transfer_variable)
        self.batch_generator.register_batch_generator(self.transfer_variable)
        self.gradient_procedure.register_gradient_procedure(self.transfer_variable)
        self.loss_computer.register_loss_procedure(self.transfer_variable, self)

    def renew_current_info(self, iter_num, batch_index):
        self.gradient_procedure.renew_current_info(iter_num, batch_index)
        self.loss_computer.renew_current_info(iter_num, batch_index)