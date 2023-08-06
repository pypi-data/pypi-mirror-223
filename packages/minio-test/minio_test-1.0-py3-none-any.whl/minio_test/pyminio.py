# -*- coding: utf-8 -*-
# @time:   2023/8/4 14:53
# @author: Zx

import sys
import traceback
from minio import Minio
from minio_test.common.common import logger


def up_file(local_path: str, minio_conf: dict):
    try:
        bucket = "file-system"
        remote_path = local_path.split("/")[-1]
        client = Minio(**minio_conf)

        # Make 'asiatrip' bucket if not exist.
        found = client.bucket_exists(bucket)
        if not found:
            client.make_bucket(bucket)
        else:
            logger.info("Bucket {} already exists".format(bucket))

        client.fput_object(
            bucket, remote_path, local_path,
        )
        logger.info(
            "{} is successfully uploaded as "
            "object {} to bucket {}.".format(local_path, remote_path, bucket)
        )
        result_path = "/minio/{}/{}".format(bucket, remote_path)
        return result_path
    except Exception as e:
        logger.error(
            "*** minio上传文件异常 -> {} {}".format(str(e), traceback.format_exc()))
        sys.exit(1)
