load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "simplified_planning",
    srcs = ["simplified_planning.py"],
    deps = [
        "//cyber/python/cyber_py3:cyber",
        "//modules/planning/proto:planning_py_pb2"
    ],
)

py_binary(
    name = "record_node",
    srcs = ["record_node.py"],
    deps = [
        "//cyber/python/cyber_py3:cyber",
        "//cyber/python/cyber_py3:record",
        "//modules/planning/proto:planning_py_pb2",
        "//modules/prediction/proto:prediction_obstacle_py_pb2",
        "//modules/perception/proto:perception_obstacle_py_pb2",
        "//modules/perception/proto:traffic_light_detection_py_pb2",
        "//modules/localization/proto:localization_py_pb2",
        "//modules/tools/common:message_manager"
    ],
)
