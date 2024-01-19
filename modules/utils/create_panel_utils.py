import asyncio


async def run_command_with_io(input_file=None, output_file=None, *args):
    """Запуск команды с вводом и выводом"""

    print(f"Running command: {' '.join(args)}")

    stdin = asyncio.subprocess.PIPE if input_file else None
    stdout = asyncio.subprocess.PIPE if output_file else None

    process = await asyncio.create_subprocess_exec(
        *args,
        stdin=stdin,
        stdout=stdout,
        stderr=asyncio.subprocess.PIPE
    )

    if input_file:
        with open(input_file, 'rb') as f:
            input_data = f.read()
        stdout, stderr = await process.communicate(input=input_data)
    else:
        stdout, stderr = await process.communicate()

    if process.returncode != 0:
        if stderr:
            print(f"Command failed with error: {stderr.decode()}")
    else:
        if output_file:
            with open(output_file, 'wb') as f:
                f.write(stdout)
        print(f"Command succeeded with output: {stdout.decode() if stdout else ''}")
