function _mycomplete_nanomerge
    set -l cur (commandline -ct)
    set -l prev (commandline -ct | sed -n '$p')
    set -l opts "--slurm-cores-per-job --slurm-queue --slurm-memory --profile --jobs --working-directory ptainer --apptainer-prefix --apptainer-args --input-directory --input-pattern --run-mode --version --from-project --samplesheet --summary --summary-percentage --summary-max-gb --run"

    switch "$prev"
        case "--profile"
            complete -c sequana_nanomerge -a "local slurm" -x
            return 0
        case "--working-directory"
            complete -c sequana_nanomerge -f -X '.[!.]*' -d -x
            return 0
        case "--input-directory"
            complete -c sequana_nanomerge -f -X '.[!.]*' -d -x
            return 0
        case "--run-mode"
            complete -c sequana_nanomerge -a "local slurm" -x
            return 0
        case "--level"
            complete -c sequana_nanomerge -a "INFO DEBUG WARNING ERROR CRITICAL" -x
            return 0
        case "--from-project"
            complete -c sequana_nanomerge -f -X '.[!.]*' -d -x
            return 0
    end

    complete -c sequana_nanomerge -f -a "$opts" -x
    return 0
end

complete -c sequana_nanomerge -n "_mycomplete_nanomerge"

