SOURCE_PATH := "userpic.py"
TEST_PATH := "test_userpic.py"

upgrade:
    uv lock --upgrade

lint:
    uv run ruff check {{ SOURCE_PATH }}
    uv run python -m mypy --pretty {{ SOURCE_PATH }}

fix:
    uv run ruff format {{ SOURCE_PATH }} {{ TEST_PATH }}
    uv run ruff check --fix --unsafe-fixes {{ SOURCE_PATH }}

tests:
    uv run pytest test_userpic.py


# Generate images with different parameters
examples:
    #!/usr/bin/env bash
    .venv/bin/python -c '
    from userpic import make_userpic_image
    # Basic black and white image
    make_userpic_image(
        size=(7, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="black"
    ).save("examples/basic.png")

    # Colored image
    make_userpic_image(
        size=(7, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="#f0f0f0",
        foreground="#2ecc71"
    ).save("examples/colored.png")

    # Image with transparent background
    make_userpic_image(
        size=(7, 5),
        mode="RGBA",
        image_size=(300, 300),
        padding=(20, 20),
        background=(255, 255, 255, 0),
        foreground=(0, 0, 128, 255)
    ).save("examples/transparent.png")

    # Image with large pattern size
    make_userpic_image(
        size=(12, 12),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="#e74c3c"
    ).save("examples/large.png")

    # Image with small pattern size
    make_userpic_image(
        size=(5, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="#f1c40f"
    ).save("examples/small.png")

    # Random image
    make_userpic_image(
        size=(7, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="#9b59b6"
    ).save("examples/random.png")

    # Image with fixed seed
    make_userpic_image(
        size=(7, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="#1abc9c",
        seed=42
    ).save("examples/seeded.png")
    '
