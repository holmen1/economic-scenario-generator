
from python import Python


fn main() raises:
    let np = Python.import_module("numpy")
    let x = np.linspace(0, 10, 100)
    let y = np.sin(x)
    plot(x, y)


def plot(x: PythonObject, y: PythonObject) -> None:
    let plt = Python.import_module("matplotlib.pyplot")
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Plot of y = sin(x)")
    plt.grid(True)
    plt.show()