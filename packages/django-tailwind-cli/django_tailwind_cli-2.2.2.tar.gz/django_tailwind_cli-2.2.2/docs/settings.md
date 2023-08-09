---
hide:
  - navigation
---

# Settings & Configuration

## Settings

The package can be configured by a few settings, which can be overwritten in the `settings.py` of your project.

`TAILWIND_VERSION`
: **Default**: `"3.3.3"`

    This defines the version of the CLI and of Tailwind CSS you want to use in your project.

`TAILWIND_CLI_PATH`
: **Default**: `"~/.local/bin/"`

    The path where to store CLI binary on your machine. The default value aims for an installation in your home directory and is tailored for Unix and macOS systems. On Windows you might need to configure a different path.

`TAILWIND_CLI_SRC_CSS`
: **Default**: `None`

    The name of the optional input file for the Tailwind CLI, where all the directivces and custom styles are defined. This is where you add your own definitions for the different layers.

    If you don't define this setting, the default of the Tailwind CLI is used.

`TAILWIND_CLI_DIST_CSS`
: **Default**: `"css/styles.css"`

    The name of the output file. This file is stored relative to the first element of the `STATICFILES_DIRS` array.

`TAILWIND_CLI_CONFIG_FILE`
: **Default**: `"tailwind.config.js"`

    The name of the Tailwind CLI config file. The file is stored relative to the `BASE_DIR` defined in your settings.

## `tailwind.config.js`

If you don't create a `tailwind.config.js` file yourself, the management commands will create a sane default for you inside the `BASE_DIR` of your project. The default activates all the official plugins for Tailwind CSS and adds a minimal plugin to support some variants for [HTMX](https://htmx.org/).

The default configuration also embrasses the nice trick authored by Carlton Gibson in his post [Using Django’s template loaders to configure Tailwind¶](https://noumenal.es/notes/tailwind/django-integration/). The implementation adopts Carlton's implementation to honor the conventions of this project. If you put your `tailwind.config.js` in a different location then your `BASE_DIR`, you have to change this file too.

This configuration uses the management command `tailwind list_templates`, which list all the templates files inside your project.

```javascript title="tailwind.config.js"
/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");
const { spawnSync } = require("child_process");

// Calls Django to fetch template files
const getTemplateFiles = () => {
  const command = "python3";
  const args = ["-m", "django", "tailwind", "list_templates"];
  // Assumes tailwind.config.js is located in the BASE_DIR of your Django project.
  const options = { cwd: __dirname };

  const result = spawnSync(command, args, options);

  if (result.error) {
    throw result.error;
  }

  if (result.status !== 0) {
    console.log(result.stdout.toString(), result.stderr.toString());
    throw new Error(
      `Django management command exited with code ${result.status}`
    );
  }

  const templateFiles = result.stdout
    .toString()
    .split("\n")
    .map((file) => file.trim())
    .filter(function (e) {
      return e;
    }); // Remove empty strings, including last empty line.
  return templateFiles;
};

module.exports = {
  content: [].concat(getTemplateFiles()),
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/container-queries"),
    plugin(function ({ addVariant }) {
      addVariant("htmx-settling", ["&.htmx-settling", ".htmx-settling &"]);
      addVariant("htmx-request", ["&.htmx-request", ".htmx-request &"]);
      addVariant("htmx-swapping", ["&.htmx-swapping", ".htmx-swapping &"]);
      addVariant("htmx-added", ["&.htmx-added", ".htmx-added &"]);
    }),
  ],
};
```
