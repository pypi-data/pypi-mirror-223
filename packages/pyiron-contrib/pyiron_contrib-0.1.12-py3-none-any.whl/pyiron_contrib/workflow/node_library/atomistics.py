from __future__ import annotations

from typing import Optional

from pyiron_atomistics import Project, _StructureFactory
from pyiron_atomistics.atomistics.job.atomistic import AtomisticGenericJob
from pyiron_atomistics.atomistics.structure.atoms import Atoms
from pyiron_atomistics.lammps.lammps import Lammps as LammpsJob

from pyiron_contrib.workflow.function import single_value_node, slow_node


@single_value_node(output_labels="structure")
def bulk_structure(element: str = "Fe", cubic: bool = False, repeat: int = 1) -> Atoms:
    return _StructureFactory().bulk(element, cubic=cubic).repeat(repeat)


@single_value_node(output_labels="job")
def lammps(structure: Optional[Atoms] = None) -> LammpsJob:
    pr = Project(".")
    job = pr.atomistics.job.Lammps("NOTAREALNAME")
    job.structure = structure if structure is not None else _StructureFactory().bulk()
    job.potential = job.list_potentials()[0]
    return job


def _run_and_remove_job(job, modifier: Optional[callable] = None, **modifier_kwargs):
    """
    Extracts the commonalities for all the "calc" methods for running a Lammps engine.
    Will need to be extended/updated once we support other engines so that more output
    can be parsed. Output may wind up more concretely packaged, e.g. as `CalcOutput` or
    `MDOutput`, etc., ala Joerg's suggestion later, so for the time being we don't put
    too much effort into this.

    Warning:
        Jobs are created in a dummy project with a dummy name and are all removed at the
        end; this works fine for serial workflows, but will need to be revisited --
        probably with naming based on the parantage of node/workflow labels -- once
        other non-serial execution is introduced.
    """
    job_name = "JUSTAJOBNAME"
    pr = Project("WORKFLOWNAMEPROJECT")
    job = job.copy_to(project=pr, new_job_name=job_name, delete_existing_job=True)
    if modifier is not None:
        job = modifier(job, **modifier_kwargs)
    job.run()

    cells = job.output.cells
    displacements = job.output.displacements
    energy_pot = job.output.energy_pot
    energy_tot = job.output.energy_tot
    force_max = job.output.force_max
    forces = job.output.forces
    indices = job.output.indices
    positions = job.output.positions
    pressures = job.output.pressures
    steps = job.output.steps
    temperature = job.output.temperature
    total_displacements = job.output.total_displacements
    unwrapped_positions = job.output.unwrapped_positions
    volume = job.output.volume

    job.remove()
    pr.remove(enable=True)

    return (
        cells,
        displacements,
        energy_pot,
        energy_tot,
        force_max,
        forces,
        indices,
        positions,
        pressures,
        steps,
        temperature,
        total_displacements,
        unwrapped_positions,
        volume,
    )


@slow_node(
    output_labels=[
        "cells",
        "displacements",
        "energy_pot",
        "energy_tot",
        "force_max",
        "forces",
        "indices",
        "positions",
        "pressures",
        "steps",
        "temperature",
        "total_displacements",
        "unwrapped_positions",
        "volume",
    ]
)
def calc_static(
    job: AtomisticGenericJob,
):
    return _run_and_remove_job(job=job)


@slow_node(
    output_labels=[
        "cells",
        "displacements",
        "energy_pot",
        "energy_tot",
        "force_max",
        "forces",
        "indices",
        "positions",
        "pressures",
        "steps",
        "temperature",
        "total_displacements",
        "unwrapped_positions",
        "volume",
    ]
)
def calc_md(
    job: AtomisticGenericJob,
    n_ionic_steps: int = 1000,
    n_print: int = 100,
    temperature: int | float = 300.0,
    pressure: float
    | tuple[float, float, float]
    | tuple[float, float, float, float, float, float]
    | None = None,
):
    def calc_md(job, n_ionic_steps, n_print, temperature, pressure):
        job.calc_md(
            n_ionic_steps=n_ionic_steps,
            n_print=n_print,
            temperature=temperature,
            pressure=pressure,
        )
        return job

    return _run_and_remove_job(
        job=job,
        modifier=calc_md,
        n_ionic_steps=n_ionic_steps,
        n_print=n_print,
        temperature=temperature,
        pressure=pressure,
    )


nodes = [
    bulk_structure,
    calc_md,
    calc_static,
    lammps,
]
