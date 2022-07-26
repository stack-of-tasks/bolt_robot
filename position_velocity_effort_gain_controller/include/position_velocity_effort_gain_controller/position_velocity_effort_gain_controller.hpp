// Copyright 2020 PAL Robotics S.L.
// Copyright 2022 LAAS CNRS.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef POSITION_VELOCITY_EFFORT_GAIN_CONTROLLER_HPP_
#define POSITION_VELOCITY_EFFORT_GAIN_CONTROLLER_HPP_

#include <memory>
#include <string>
#include <vector>


#include "controller_interface/controller_interface.hpp"
#include "forward_command_controller/visibility_control.h"
#include "rclcpp/subscription.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"
#include "realtime_tools/realtime_buffer.h"
#include "std_msgs/msg/float64_multi_array.hpp"
#include <system_interface_bolt.hpp>
#include "controller_interface/helpers.hpp"

namespace position_velocity_effort_gain_controller{

    using CmdType = std_msgs::msg::Float64MultiArray;
    using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

    class PosVelTorGainsController: public controller_interface::ControllerInterface{

        public:
            std::vector<std::string> joint_names_;
            std::vector<std::string> interface_names_;

            std::vector<std::string> command_interface_types_;

            //if we want a matrix instead of a long vector, since we have several joints and interfaces :
            //std::vector<std::vector<std::string>> command_interface_types_; 

            realtime_tools::RealtimeBuffer<std::shared_ptr<CmdType>> rt_command_ptr_;
            rclcpp::Subscription<CmdType>::SharedPtr joints_command_subscriber_;

        public:

            PosVelTorGainsController();

            ~PosVelTorGainsController() = default;

            controller_interface::InterfaceConfiguration command_interface_configuration() const override;

            controller_interface::InterfaceConfiguration state_interface_configuration() const override;

            controller_interface::return_type init(const std::string & controller_name);

            CallbackReturn on_configure(
            const rclcpp_lifecycle::State & previous_state) ;

            CallbackReturn on_activate(
            const rclcpp_lifecycle::State & previous_state) ;

            CallbackReturn on_deactivate(
            const rclcpp_lifecycle::State & previous_state) ;

            controller_interface::return_type update() override;

             void declare_parameters();

            CallbackReturn read_parameters() ;

    };

}

#endif
