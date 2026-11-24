# generated from causaliq@7783c42bf150 src/causaliq/devtools/templates.py - do not edit
param(
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$Args
)

& python "$PSScriptRoot\check_ci.py" @Args
exit $LASTEXITCODE
