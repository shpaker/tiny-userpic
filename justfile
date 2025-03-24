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


# Генерируем изображения с разными параметрами
examples:
    #!/usr/bin/env bash
    .venv/bin/python -c '
    from userpic import make_userpic_image
    # Базовое черно-белое изображение
    make_userpic_image(
        size=(7, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="black"
    ).save("examples/basic.png")

    # Цветное изображение
    make_userpic_image(
        size=(7, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="#f0f0f0",
        foreground="#2ecc71"
    ).save("examples/colored.png")

    # Изображение с прозрачным фоном
    make_userpic_image(
        size=(7, 5),
        mode="RGBA",
        image_size=(300, 300),
        padding=(20, 20),
        background=(255, 255, 255, 0),
        foreground=(0, 0, 128, 255)
    ).save("examples/transparent.png")

    # Изображение с большим размером паттерна
    make_userpic_image(
        size=(12, 12),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="#e74c3c"
    ).save("examples/large.png")

    # Изображение с маленьким размером паттерна
    make_userpic_image(
        size=(5, 5),
        mode="RGB",
        image_size=(300, 300),
        padding=(20, 20),
        background="white",
        foreground="#f1c40f"
    ).save("examples/small.png")
    '
