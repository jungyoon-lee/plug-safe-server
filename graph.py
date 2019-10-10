import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import io
import base64


def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()

    plt.fill_between(range(len(y_coordinates)), y_coordinates, 0, color='green', alpha=0.7)
    plt.xticks([])

    plt.savefig(img, format='png')

    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return 'data:image/png;base64,{}'.format(graph_url)