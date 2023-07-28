# File_Tree

File Tree's are a way to specify convention for data structures and naming schemes.
If you are interested you can find the documentation [here](https://pypi.org/project/file-tree/).
However, I would recommend reading this documentation instead because not all of the file_tree
features are used in the utility and you may find some differences in the way things are handled
here.
There are further ways to increase robustness of this tool using file_tree functionality, so
expect this section to evolve in the future.

## Placeholders

Placeholders are a way denote portions of directory and file names that may vary. A common
instance of this is subject ID's. i.e. sub-01, sub-02. The portion of '01' and '02' is the
place holder.
There are two kinds of placeholders: required and optional.

### Required Placeholders

Required placeholders, as the name implies, are segments that must exist in order to make
a match between a file/directory and a template name.
Required placeholders are denoted by curly braces '{}'.
Example:
```
identity-{required identity}
```

### Optional Placeholders

Optional placeholders, conversely, are segments that may or may not exist in order to find a
match between a file/directory and a template name.
Optional placeholders are denoted by square braces '[]'.
They are useful for options in names that might exist but don't always have to.
Example:
```
[optional-{placeholder}]
```
## Subtrees

With file trees it is possible to reference a file tree within another. This is useful for
mainting clarity for large data structures. A subtree must be located within the same folder
the parent file tree. To reference a sub tree the following expression is used: '-> {subtree name}'
Example:
```
parent-{parent_id}
    [optional-{optional sub directory}]
        -> subtree
```

## Identifiers

Identifiers are the "nicknames" used to reference a file/directory template name. These can
be specified within the file tree using '()'. They will be automatically generated if none is
given by removing an extension. The specifics of this can be found [here](https://git.fmrib.ox.ac.uk/ndcn0236/file-tree/-/blob/master/src/file_tree/template.py#:~:text=def%20guess_key(,)%5B0%5D) in the guess_key function.
It is highly recommended to supply these "nicknames" for clarity.
Example:
```
subject-{subject}_important-processed-data.data (processed_data)
```

## Example Trees
Several example trees are included with the file_tree_check passage.
Example of bids_raw tree:
```
ext=.nii.gz
participant = 1, 2, 3, 4, 5, 6, 7, 8
dataset_description.json
participants.tsv
README (readme)
CHANGES (changes)
LICENSE (license)
genetic_info.json
sub-{participant}
    [ses-{session}]
        sub-{participant}_sessions.tsv (sessions_tsv)
        anat (anat_dir)
            sub-{participant}[_ses-{session}][_acq-{acq}][_ce-{ce}][_rec-{rec}][_run-{run_index}]_{modality}{ext} (anat_image)
            sub-{participant}[_ses-{session}][_acq-{acq}][_ce-{ce}][_rec-{rec}][_run-{run_index}][_mod-{modality}]_defacemask{ext} (anat_deface)
        func (func_dir)
            sub-{participant}[_ses-{session}]_task-{task}[_acq-{acq}][_ce-{ce}][_dir-{dir}][_rec-{rec}][_run-{run_index}][_echo-{echo}]_bold.nii.gz (task_image)
            sub-{participant}[_ses-{session}]_task-{task}[_acq-{acq}][_ce-{ce}][_dir-{dir}][_rec-{rec}][_run-{run_index}][_echo-{echo}]_bold.json  (task_image_json)
            sub-{participant}[_ses-{session}]_task-{task}[_acq-{acq}][_ce-{ce}][_dir-{dir}][_rec-{rec}][_run-{run_index}][_echo-{echo}]_sbref{ext} (task_sbref)
            sub-{participant}[_ses-{session}]_task-{task}[_acq-{acq}][_ce-{ce}][_dir-{dir}][_rec-{rec}][_run-{run_index}][_echo-{echo}]_events.tsv  (task_events)
            sub-{participant}[_ses-{session}]_task-{task}[_acq-{acq}][_ce-{ce}][_dir-{dir}][_rec-{rec}][_run-{run_index}][_echo-{echo}][_recording-{recording}]_physio.tsv.gz (task_physio)
            sub-{participant}[_ses-{session}]_task-{task}[_acq-{acq}][_ce-{ce}][_dir-{dir}][_rec-{rec}][_run-{run_index}][_echo-{echo}][_recording-{recording}]_stim.tsv.gz (task_stim)
            sub-{participant}[_ses-{session}]_task-{task}[_acq-{acq}][_ce-{ce}][_dir-{dir}][_rec-{rec}][_run-{run_index}][_echo-{echo}]_desc-confounds_{confounds}.tsv (desc-confounds)
        dwi (dwi_dir)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_dwi{ext} (dwi_image)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_dwi.bval (bval)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_dwi.bvec (bvec)
        fmap (fmap_dir)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_phasediff{ext} (fmap_phasediff)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_magnitude{ext} (fmap_mag)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_magnitude1{ext} (fmap_mag1)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_magnitude2{ext} (fmap_mag2)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_phase1{ext} (fmap_phase1)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_phase2{ext} (fmap_phase2)
            sub-{participant}[_ses-{session}][_acq-{acq}][_run-{run_index}]_fieldmap{ext} (fmap)
            sub-{participant}[_ses-{session}][_acq-{acq}]_dir-{dir}[_run-{run_index}]_epi{ext} (fmap_epi)
        meg (meg_dir)
            sub-{participant}[_ses-{session}]_task-{task}[_run-{run}][_proc-{proc}]_meg.{meg_ext} (meg)
        eeg (eeg_dir)
            sub-{participant}[_ses-{session}]_task-{task}[_run-{run}][_proc-{proc}]_eeg.{eeg_ext} (eeg)
        ieeg (ieeg_dir)
            sub-{participant}[_ses-{session}]_task-{task}[_run-{run}][_proc-{proc}]_ieeg.{ieeg_ext} (ieeg)
        beh (behavioral_dir)
            sub-{participant}[_ses-{session}]_task-{task}_events.tsv (behavioural_events)
            sub-{participant}[_ses-{session}]_task-{task}_beh.tsv (behavioural)
            sub-{participant}[_ses-{session}]_task-{task}_physio.tsv.gz (behavioural_physio)
            sub-{participant}[_ses-{session}]_task-{task}_stim.tsv.gz (behavioral_stim)

```
More examples can be found [here](https://git.fmrib.ox.ac.uk/fsl/fslpy/-/tree/master/fsl/utils/filetree/trees)
