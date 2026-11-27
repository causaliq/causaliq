# generated from causaliq@a7fc1db88992da9d8accb50690aa204212bd3d00 src/causaliq/devtools/templates.py - do not edit
param(
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$Args
)

& python "$PSScriptRoot\check_ci.py" @Args
exit $LASTEXITCODE
