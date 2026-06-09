import os
import traceback
import logging
import subprocess
from utils.ffmpeg_helper import FFMPEG, FFPROBE


logger = logging.getLogger(__name__)

import ffmpeg
import torch

from configs.config import Config
from infer.modules.uvr5.mdxnet import MDXNetDereverb
from infer.modules.uvr5.preprocess import AudioPre, AudioPreDeEcho

config = Config()



def uvr(model_name, inp_root, save_root_vocal, paths, save_root_ins, agg, format0):
    infos = []

    try:
        inp_root = inp_root.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        save_root_vocal = (
            save_root_vocal.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )
        save_root_ins = (
            save_root_ins.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        )
        if model_name == "onnx_dereverb_By_FoxJoy":
            pre_fun = MDXNetDereverb(15, config.device)
        else:
            func = AudioPre if "DeEcho" not in model_name else AudioPreDeEcho
            pre_fun = func(
                agg=int(agg),
                model_path=os.path.join(
                    os.getenv("weight_uvr5_root"), model_name + ".pth"
                ),
                device=config.device,
                is_half=config.is_half,
            )
        if inp_root != "":
            paths = [os.path.join(inp_root, name) for name in os.listdir(inp_root)]
        else:
            paths = [path.name for path in paths]
        for path in paths:
            inp_path = os.path.join(inp_root, path)
            need_reformat = 1
            done = 0
            try:
                info = ffmpeg.probe(inp_path, cmd=FFPROBE)
                if (
                    info["streams"][0]["channels"] == 2
                    and info["streams"][0]["sample_rate"] == "44100"
                ):
                    need_reformat = 0
                    pre_fun._path_audio_(
                        inp_path, save_root_ins, save_root_vocal, format0
                    )
                    done = 1
                infos.append(f"{os.path.basename(inp_path)}->Success")
                msg = "\n".join(infos)
                logger.info("FIRST YIELD")
                logger.info(f"YIELDING: {msg}")
                return msg
            except Exception:
                infos.append(f"{os.path.basename(inp_path)}->{traceback.format_exc()}")
                msg = "\n".join(infos)
                logger.info(f"YIELDING: {msg}")
                return msg
            if need_reformat == 1:
                tmp_dir = os.getenv("TEMP") or "/tmp"

                tmp_path = os.path.join(
                    tmp_dir,
                    f"{os.path.basename(inp_path)}.reformatted.wav"
                )
                result = subprocess.run([
                    FFMPEG,
                    "-y",
                    "-i", inp_path,
                    "-vn",
                    "-acodec", "pcm_s16le",
                    "-ac", "2",
                    "-ar", "44100",
                    tmp_path
                ], capture_output=True)

                if result.returncode != 0:
                    raise RuntimeError(f"FFmpeg failed: {result.stderr.decode()}")
                inp_path = tmp_path
            try:
                if done == 0:
                    pre_fun._path_audio_(
                        inp_path, save_root_ins, save_root_vocal, format0
                    )
                infos.append("%s->Success" % (os.path.basename(inp_path)))
                msg = "\n".join(infos)
                logger.info("SECOND YIELD")
                logger.info(f"YIELDING: {msg}")
                return msg
            except:
                try:
                    if done == 0:
                        pre_fun._path_audio_(
                            inp_path, save_root_ins, save_root_vocal, format0
                        )
                    infos.append("%s->Success" % (os.path.basename(inp_path)))
                    msg = "\n".join(infos)
                    logger.info(f"YIELDING: {msg}")
                    return msg
                except:
                    infos.append(
                        "%s->%s" % (os.path.basename(inp_path), traceback.format_exc())
                    )
                    msg = "\n".join(infos)
                    logger.info(f"YIELDING: {msg}")
                    return msg
        logger.info("UVR FUNCTION FINISHED")
    except GeneratorExit:
        logger.info("Generator closed by Gradio")
        return
    except Exception:
        infos.append(traceback.format_exc())
        msg = "\n".join(infos)
        logger.info(f"YIELDING: {msg}")
        return msg

    finally:
        try:
            if 'pre_fun' in locals():
                if model_name == "onnx_dereverb_By_FoxJoy":
                    if hasattr(pre_fun, "pred"):
                        if hasattr(pre_fun.pred, "model"):
                            del pre_fun.pred.model
                        if hasattr(pre_fun.pred, "model_"):
                            del pre_fun.pred.model_
                else:
                    if hasattr(pre_fun, "model"):
                        del pre_fun.model
                    del pre_fun
        except:
            traceback.print_exc()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("UVR CLEANUP FINISHED")


