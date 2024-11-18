import gradio as gr
import sys, os
from tabs.full_inference import full_inference_tab
from tabs.download_model import download_model_tab

now_dir = os.getcwd()
sys.path.append(now_dir)
DEFAULT_PORT = 7755
MAX_PORT_ATTEMPTS = 10

from assets.i18n.i18n import I18nAuto

i18n = I18nAuto()


with gr.Blocks(title="hexGen-RVC", css="footer{display:none !important}") as app:
    gr.Markdown("# hexGen RVC")
    with gr.Tab(i18n("Full Inference")):
        full_inference_tab()
    with gr.Tab(i18n("Download Model")):
        download_model_tab()


print("launching app...")
def launch(port):
    app.launch(
        share="--share" in sys.argv,
        inbrowser="--open" in sys.argv,
        server_port=port,
    )


def get_port_from_args():
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port") + 1
        if port_index < len(sys.argv):
            return int(sys.argv[port_index])
    return DEFAULT_PORT


if __name__ == "__main__":
    port = get_port_from_args()
    for _ in range(MAX_PORT_ATTEMPTS):
        try:
            launch(port)
            break
        except OSError:
            print(
                f"Failed to launch on port {port}, trying again on port {port - 1}..."
            )
            port -= 1
        except Exception as error:
            print(f"An error occurred launching Gradio: {error}")
            break
