# genenv
Generate environment variable files automatically from a template and Azure DevOps library variables

# Usage
Install wheel file available at [Releases](https://github.com/edgar-g-q/genenv/releases).
From this point, you should be able to run the tool by writing the following in a terminal
```bash
genenv
```
To view the full list of options, write
```bash
genenv -h
```
The main arguments you need to provide are:

- template file (--template, -t) used to generate the environment variables file. It should have jinja-like syntax. If not provided, the tool will ask for it either through a file dialog or through console.
- azure variable group name (--group, -g). You can list available groups through option (--list-groups, -l)
- genenv configuration file (--config, -c). JSON configuration file with azure token, secrets and additional configuration.

If you want to skip providing configuration file each time as an argument, you can create it at your user home directory, with the name ".genenv.json".

The configuration file shall have, at least, values for "azure_organization" and for "azure_token".
In "azure_organization", enter the name of the organization you are working with. In "azure_token", enter your Azure Personal Access Token, which shall have access for reading variable groups. Check Azure DevOps documentation for more information.

Additionally, in case your variable groups have some secret values for some of the environment variables, you may need to enter these values at the configuration file, for each variable group. Below you can find an example of configuration file.

```json
{
	"azure_organization": "[YOUR_AZURE_ORGANIZATION]",
	"azure_token": "[YOUR_AZURE_TOKEN]",
    "default_variable_group": "[DEFAULT_AZURE_VARIABLE_GROUP]",
	"secrets": {
	  "[AZURE_VARIABLE_GROUP_1]": {
		"[SECRET_1]": "[SECRET_1_VALUE]",
        "[SECRET_2]": "[SECRET_2_VALUE]"
	  },
	  "[AZURE_VARIABLE_GROUP_2]": {
        "[SECRET_1]": "[SECRET_1_VALUE]",
        "[SECRET_2]": "[SECRET_2_VALUE]"
      }
	}
}
```


