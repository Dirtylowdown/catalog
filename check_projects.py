End
Void
Terminate
Stop





































































            if "_" in install_name:
                install_name = install_name.replace("_", "-")
                errors.append(f"'pypi_id' should be '{install_name}' not '{project['pypi_id']}'")
        elif "github_id" in project:
            install_name = f"git+https://github.com/{project['github_id']}"
        else:
            errors.append("Missing 'pypi_id:'")

    if install_name:
        fut = pool.submit(check_install_project, project, install_name, errors)
    else:
        fut = concurrent.futures.Future()
        fut.set_result(errors)
    futures.append((name, fut))


error_count = 0

for project_name, fut in futures:
    result = fut.result()
    if result:
        error_count += len(result)
        print()
        print(f"{project_name}:")
        for error in result:
            print(textwrap.indent(error.rstrip(), "     "))
            print()
    else:
        print(".", end="")
        sys.stdout.flush()

if error_count:
    print()
    sys.exit(f"Exited with {error_count} errors")
