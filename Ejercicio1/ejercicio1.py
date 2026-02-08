import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

TORUS_OUTER_RADIUS=1.5
TORUS_INNER_RADIUS=0.5
SPHERE_RADIUS=0.5
EXACT_TORUS_VOLUME=2*np.pi**2*TORUS_OUTER_RADIUS*TORUS_INNER_RADIUS**2
EXACT_SPHERE_VOLUME=(4/3)*np.pi*SPHERE_RADIUS**3
LEFT_SPHERE_OFFSET=-2
RIGHT_SPHERE_OFFSET=2
TORUS_SPHERE_ANALYSIS_NSIMS=1000000
TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF=3
PROBABILITY_MASS=(TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF*2)**3

def is_within_right_sphere(x,y,z) -> bool:
    return (x-RIGHT_SPHERE_OFFSET)**2 + y**2 + z**2 <= SPHERE_RADIUS**2

def is_within_left_sphere(x,y,z) -> bool:
    return (x-LEFT_SPHERE_OFFSET)**2 + y**2 + z**2 <= SPHERE_RADIUS**2

def is_within_torus(x,y,z) -> bool:
    return (x**2+y**2+z**2 + TORUS_OUTER_RADIUS**2 -TORUS_INNER_RADIUS**2)**2 <= 4*TORUS_OUTER_RADIUS**2*(x**2+y**2)


def montecarlo_torus_spheres_analysis():
    torus_hits=0
    right_sphere_hits=0
    left_sphere_hits=0
    intersection_torus_right_sphere_hits=0
    intersection_torus_left_sphere_hits=0
    union_hits=0

    # Compute the Monte Carlo estimation of the volumes by sampling points in a cube that contains all the objects (toro and spheres)
    # and counting how many points fall within each object, their intersections, and their union.
    for _ in range(TORUS_SPHERE_ANALYSIS_NSIMS):
        x = np.random.uniform(-TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF, TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF)
        y =  np.random.uniform(-TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF, TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF)
        z =  np.random.uniform(-TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF, TORUS_SPHERE_ANALYSIS_CUBE_SIDE_HALF)
        
        hit_torus = is_within_torus(x, y, z)
        hit_right = is_within_right_sphere(x, y, z)
        hit_left  = is_within_left_sphere(x, y, z)

        torus_hits += hit_torus
        right_sphere_hits += hit_right
        left_sphere_hits += hit_left
        if hit_torus or hit_right or hit_left:
            union_hits += 1

        if hit_torus:
            if hit_right: intersection_torus_right_sphere_hits += 1
            if hit_left:  intersection_torus_left_sphere_hits  += 1

    print("--- Monte Carlo Torus and Spheres Analysis ---")
    # 1.2 Torus volume estimation
    torus_estimated_volume=PROBABILITY_MASS*torus_hits/TORUS_SPHERE_ANALYSIS_NSIMS
    torus_absolute_error = abs(EXACT_TORUS_VOLUME-torus_estimated_volume)
    torus_relative_error_percentage = 100*torus_absolute_error/EXACT_TORUS_VOLUME
    print("--- Torus Volume Estimation ---")
    print('Number of samples:',TORUS_SPHERE_ANALYSIS_NSIMS)
    print('Estimated torus volume:',torus_estimated_volume)
    print('Exact torus volume:',EXACT_TORUS_VOLUME)
    print('Relative error torus:',torus_relative_error_percentage, '%')
    print()

    # 1.3 Sphere volume estimation
    right_sphere_estimated_volume = PROBABILITY_MASS*right_sphere_hits/TORUS_SPHERE_ANALYSIS_NSIMS
    right_sphere_absolute_error = abs(EXACT_SPHERE_VOLUME-right_sphere_estimated_volume)
    right_sphere_relative_error_percentage = 100*right_sphere_absolute_error/EXACT_SPHERE_VOLUME

    left_sphere_estimated_volume=PROBABILITY_MASS*left_sphere_hits/TORUS_SPHERE_ANALYSIS_NSIMS
    left_sphere_absolute_error = abs(EXACT_SPHERE_VOLUME-left_sphere_estimated_volume)
    left_sphere_relative_error_percentage = 100*left_sphere_absolute_error/EXACT_SPHERE_VOLUME

    values = [right_sphere_estimated_volume, left_sphere_estimated_volume]
    sphere_estimated_volume_difference_percentage = 100*(np.abs(np.diff(values)) / np.mean(values))[0]

    print("--- Sphere Volume Estimation ---")
    print('Estimated right sphere volume:',right_sphere_estimated_volume)
    print('Estimated left sphere volume:',left_sphere_estimated_volume)
    print('Exact sphere volume:',EXACT_SPHERE_VOLUME)
    print('Relative error percentage sphere right:',right_sphere_relative_error_percentage, '%')
    print('Relative error percentage sphere left:',left_sphere_relative_error_percentage, '%')
    print('Symmetry check: relative difference between estimated volumes of the spheres:',sphere_estimated_volume_difference_percentage, '%')
    print()

    # 1.4 Torus-sphere intersection volume estimation
    intersection_torus_right_sphere_estimated_volume = PROBABILITY_MASS*intersection_torus_right_sphere_hits/TORUS_SPHERE_ANALYSIS_NSIMS
    intersection_torus_left_sphere_estimated_volume = PROBABILITY_MASS*intersection_torus_left_sphere_hits/TORUS_SPHERE_ANALYSIS_NSIMS

    values = [intersection_torus_right_sphere_estimated_volume, intersection_torus_left_sphere_estimated_volume]
    sphere_intersection_estimated_volume_difference_percentage = 100 *(np.abs(np.diff(values)) / np.mean(values))[0]

    print("--- Torus-Sphere Intersection Volume Estimation ---")
    print('Estimated torus-sphere intersection volume (right):', intersection_torus_right_sphere_estimated_volume)
    print('Estimated torus-sphere intersection volume (left):', intersection_torus_left_sphere_estimated_volume)
    print('Symmetry check: relative difference between estimated volumes of torus-sphere intersections:', sphere_intersection_estimated_volume_difference_percentage, '%')
    print()

    # 1.5 Torus-spheres union volume estimation
    union_estimated_volume = PROBABILITY_MASS*union_hits/TORUS_SPHERE_ANALYSIS_NSIMS
    print("--- Torus-Spheres Union Volume Estimation ---")
    print('Estimated torus-spheres union volume:', union_estimated_volume)
    print()
    # 1.6 Consistency check: The estimated volume of the union should be approximately equal to
    # the sum of the exact volumes of the torus and the two spheres, minus the estimated volumes of their intersections (to avoid double-counting).
    exact_volume = EXACT_TORUS_VOLUME + 2*EXACT_SPHERE_VOLUME - intersection_torus_right_sphere_estimated_volume - intersection_torus_left_sphere_estimated_volume
    values = [exact_volume, union_estimated_volume]
    union_error_percentage = 100 *(np.abs(np.diff(values)) / np.mean(values))[0]
    print("--- Consistency Check ---")
    print('Relative difference between estimated union volume and sum of exact volumes minus estimated intersections:', union_error_percentage, '%')
    print()

def montecarlo_torus_convergence_analysis():
    toro_relative_errors = []
    nsims_list = [1000, 10000, 100000, 1000000]
    for nsims in nsims_list:
        toro_relative_errors_for_nsim = []
        for _ in range(50):
            torus_hits = 0
            for _ in range(nsims):
                x = np.random.uniform(-3, 3)
                y =  np.random.uniform(-3, 3)
                z =  np.random.uniform(-3, 3)
                if is_within_torus(x,y,z):
                    torus_hits+=1
            correction_factor=6**3
            torus_estimated_volume = correction_factor*torus_hits/nsims
            toro_relative_errors_for_nsim.append(abs(EXACT_TORUS_VOLUME-torus_estimated_volume)/EXACT_TORUS_VOLUME)
        toro_relative_errors.append(np.mean(toro_relative_errors_for_nsim))

    # Print a table of the results with the number of simulations and relative error for each case.
    print("--- Monte Carlo Torus Volume Estimation Convergence ---")
    print(f"{'NSims':>10} | {'Relative Error':>15}")
    print("-" * 30)
    for nsims, rel_error in zip(nsims_list, toro_relative_errors):
        print(f"{nsims:>10} | {rel_error:>15.5f}")
    print()

    log_n = np.log(nsims_list)
    log_error = np.log(toro_relative_errors)
    slope, _, _, _, _ = linregress(log_n, log_error)

    
    # --- 5. Plotting ---
    plt.figure(figsize=(10, 6))

    # Plot the actual data
    plt.plot(log_n, log_error, 'bo-', label=f'Resultado empírico (Pendiente = {slope:.2f})', markersize=8)

    # Plot the theoretical line (Slope -0.5)
    # We anchor it to the first point to make them comparable
    theoretical_line = log_error[0] - 0.5 * (log_n - log_n[0])
    plt.plot(log_n, theoretical_line, 'r--', label='Pendiente teórica -1/2 (1/sqrt(N))', linewidth=2)

    plt.xlabel('log(N)')
    plt.ylabel('log(Error Relativo Medio)')
    plt.title('Ratio de convergencia de Monte Carlo para la estimación del volumen del toro')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.4)
    plt.show()


def main():
    montecarlo_torus_spheres_analysis()
    montecarlo_torus_convergence_analysis()

if __name__ == "__main__":
    main()