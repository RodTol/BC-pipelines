#!/bin/bash
#SBATCH --job-name=file-test-dorado
#SBATCH --time=06:00:00
#SBATCH -A dssc -p DGX --ntasks-per-node=1 --nodes=1 --cpus-per-task=256 --gpus=8 --nodelist=dgx002

run_name="run_${i}"
#OUTPUT DIR
mkdir -p /AB_20T_output/nanopore_output/run_files_test/outputs/$run_name
mkdir -p /AB_20T_output/nanopore_output/run_files_test/outputs/$run_name/pass
mkdir -p /AB_20T_output/nanopore_output/run_files_test/outputs/$run_name/fail
#GPU-CONNECTION LOG DIR
#mkdir -p /AB_20T_output/nanopore_output/run_files_test/logs/$run_name
#LOG DIR
mkdir -p /u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/bc_logs/$run_name

srun /u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/instructions.sh $i &
wait

# move supervisors logs to directory
cd /u/dssc/tolloi/Cluster_Basecalling_Manager/BC_software/orfeo_executable/file_performance_test/bc_logs
mv dgx002_* $run_name


