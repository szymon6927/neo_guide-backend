def psalm_image_directory_path(instance, filename):
    return f'psalms/{instance.psalm.id}/images/{filename}'


def psalm_audio_directory_path(instance, filename):
    return f'psalms/{instance.psalm.id}/audio/{filename}'
