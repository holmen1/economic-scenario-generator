
from python import Python



fn main() raises:
    let np = Python.import_module("numpy")
    Python.add_to_path("source/")
    #let setup = Python.import_module("setup")
    #setup.ensure_package_installed("scipy")
    let noise = Python.import_module("noise")
    let noise_generator = noise.NoiseGenerator()
    let N = 100 # simulations
    let interval = 12 # monthly
    let T = 15 # years
    let steps = interval * T

    let s0 = np.array([224.0, 234.0, 0.03]) # initial value
    let a = np.array([0.0, 0.0, 0.09]) # speed of reversion (rates)
    let mu = np.array([0.094, 0.094, -0.007]) # drift (stocks), long term mean level (rates)
    let sigma = np.array([0.16, 0.16, 0.007]) # volatility
    let corrmatrix = np.array([1.0, 1.0, 0.2, 1.0, 1.0, 0.2, 0.2, 0.2, 1.0]).reshape(3, 3)

    let dB = noise_generator.normal_steps(corrmatrix, N * steps)
    print(dB.shape)

    plot(dB)


def plot(db: PythonObject) -> None:
    let plt = Python.import_module("matplotlib.pyplot")
    plt.plot(db.T)
    plt.xlabel("time")
    plt.ylabel("noise")
    plt.title("Plot of Brownian noise")
    plt.grid(True)
    plt.show()