# generated from causaliq@693e2bfe00df-dirty src/causaliq/devtools/templates.py - do not edit
param(
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$Args
)

& python "$PSScriptRoot\check_ci.py" @Args
exit $LASTEXITCODE
