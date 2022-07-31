import taichi as ti

ti.init(arch=ti.vulkan)

X = 3200
Y = 1800
DROP = 100
CHECK = Y * 2
# pixels = ti.field(dtype=ti.f32, shape=(n * 2, n))
pixels = ti.Matrix.field(n=4, m=1, dtype=ti.f32, shape=(X, Y))

# Crashes on Vulkan
# pixels = ti.Vector.field(n, dtype=ti.f32, shape=(n*2, n))


@ti.kernel
def paint(dr: float):
    for px, py in pixels:
        r = 1 + 3 * (px / X)
        v = 0.5
        for _ in range(DROP):
            v = r * v * (1 - v)
        closest_dist = 1.0
        for _ in range(CHECK):
            v = r * v * (1 - v)
            err = ti.abs(v - py/Y)
            closest_dist = err if err < closest_dist else closest_dist
        if closest_dist <= 2 * (1 / Y):
            # print(closest_dist * Y)
            pixels[px, py][0] = ti.log(1 + closest_dist * Y)
            pixels[px, py][1] = ti.log(1 + closest_dist * Y)
            # pixels[px, py][2] = ti.sqrt(0.1 * px / X)
        # px = int(ti.round((r-1)/3 * X))
        # py = int(ti.round(v * Y))


window = ti.ui.Window('Bifurcation diagram', (X, Y))
canvas = window.get_canvas()

i = 0
while window.running:
    pixels.fill(0)
    paint(i)
    canvas.set_image(pixels)
    window.show()
    i += 0.001
    # print(i)