from .command import gather, scatter

def call_scatter():
    scatter("../example/pypi_logo.png", 3, 3)

def call_gather():
    gather("../example/comp-4.png", 2, 2, [
        "../example/output/0-0.png",
        "../example/output/0-1.png",
        "../example/output/1-0.png",
        "../example/output/1-1.png"
    ])

if __name__ == "__main__":
    call_scatter()
    call_gather()