import matplotlib.pyplot as plt
from .utils import *
from datetime import datetime
import numpy as np
import matplotlib as mpl



def auxiliar_names(covid_parameters, model_parameters):
    """
    Provides filename with timestamp and IC_analysis type
    (2: Single Run, 1: Confidence Interval, 3: Sensitivity Analysis)
    as string for files
    """
    time = datetime.today()
    time = time.strftime('%Y%m%d%H%M')    

    if model_parameters.IC_analysis == 2: # SINGLE RUN

    	beta = covid_parameters.beta				# infectiviy_rate
    	gamma = covid_parameters.gamma			# contamination_rate

    	basic_reproduction_number = beta / gamma
    	r0 = basic_reproduction_number

    	filename = (time
            + '_single_run'
    		+ '_r' + ("%.1f" % r0)[0] + '_' + ("%.1f" % r0)[2]
    		+ '__g' + ("%.1f" % gamma)[0] + '_' + ("%.1f" % gamma)[2]
    		)
    elif model_parameters.IC_analysis == 1: # CONFIDENCE INTERVAL
        filename = (time + '_confidence_interval')
    else: # SENSITIVITY_ANALYSIS
    	filename = (time + '_sensitivity_analysis')
    return filename


def plots(results, covid_parameters, model_parameters, plot_dir):

	"""
	Makes plots:
        CONFIDENCE INTERVAL AND SINGLE RUN

    1,4,7) Infected by age group for each degree of isolation
    
    2,5,8) Bed demand by age group for each degree of isolation
    
    3,6,9) Deceased by age group for each degree of isolation
    
    10) Infected for different degrees of isolation
    
    
    
        CONFIDENCE INTERVAL
    5% QUARTIL, MEDIANA, 95% QUARTIL
    
        SENSITIVITY ANALYSIS
    1) Infected people (r0)
    
    
    Degrees of isolation (i)
    no isolation, vertical, horizontal
        
    IC_Analysis
    1: Confidence Interval; 2: Single Run; 3: Sensitivity Analysis
    
    Age groups
    Elderly (60+); Young (0-59)
    
    Hospital Bed
    Ward; ICU
    
	"""
	
	N = model_parameters.population
	#capacidade_leitos = model_parameters.bed_ward
	#capacidade_UTIs = model_parameters.bed_icu
	IC_analysis = model_parameters.IC_analysis

	t_max = model_parameters.t_max
	t_space = np.arange(0, t_max)
	fig_style = "ggplot" # "ggplot" # "classic" #
	# plot
	tamfig = (8,6)     # Figure Size
	fsLabelTitle = 11   # Font Size: Label and Title
	fsPlotLegend = 10   # Font Size: Plot and Legend

	main_label_x = 'Days'
	main_label_y = 'Infected people'

	cor = ['b','r','k','g','y','m']     # Line Colors
	ls = ['-.', '-']                    # Line Style
	leg_loc = 'upper left' # 'upper right' # 'upper left' #
	filetype = '.pdf'      # '.pdf' # '.png' #
    
	
	def format_float(float_number, precision=2):
		return str(round(float_number,2)).replace(".", "")

	# 1: without; 2: vertical; 3: horizontal isolation 
	for i in range(3):
		omega_i = model_parameters.contact_reduction_elderly[i]
		omega_j = model_parameters.contact_reduction_young[i]
        
		f_omega_i = format_float(omega_i, 1)
		f_omega_j = format_float(omega_j, 1)
       
		filename = f"we_{f_omega_i}_wy_{f_omega_j}"

		main_title = f'SEIR: $\omega_e={omega_i}$, $\omega_y={omega_j}$'
		
		
		if IC_analysis == 2: # SINGLE RUN
			Si = results.query('omega_i == @omega_i & omega_j == @omega_j')['Si']
			Sj = results.query('omega_i == @omega_i & omega_j == @omega_j')['Sj']
			Ei = results.query('omega_i == @omega_i & omega_j == @omega_j')['Ei']
			Ej = results.query('omega_i == @omega_i & omega_j == @omega_j')['Ej']
			Ii = results.query('omega_i == @omega_i & omega_j == @omega_j')['Ii']
			Ij = results.query('omega_i == @omega_i & omega_j == @omega_j')['Ij']
			Ri = results.query('omega_i == @omega_i & omega_j == @omega_j')['Ri']
			Rj = results.query('omega_i == @omega_i & omega_j == @omega_j')['Rj']
			Hi = results.query('omega_i == @omega_i & omega_j == @omega_j')['Hi']
			Hj = results.query('omega_i == @omega_i & omega_j == @omega_j')['Hj']
			Ui = results.query('omega_i == @omega_i & omega_j == @omega_j')['Ui']
			Uj = results.query('omega_i == @omega_i & omega_j == @omega_j')['Uj']
			Mi = results.query('omega_i == @omega_i & omega_j == @omega_j')['Mi']
			Mj = results.query('omega_i == @omega_i & omega_j == @omega_j')['Mj']
			
		else: # SENSITIVITY ANALYSIS OR CONFIDENCE INTERVAL
		
			Si = np.zeros((len(results),t_max))
			Sj = np.zeros((len(results),t_max))
			Ei = np.zeros((len(results),t_max))
			Ej = np.zeros((len(results),t_max))
			Ii = np.zeros((len(results),t_max))
			Ij = np.zeros((len(results),t_max))
			Ri = np.zeros((len(results),t_max))
			Rj = np.zeros((len(results),t_max))
			Hi = np.zeros((len(results),t_max))
			Hj = np.zeros((len(results),t_max))
			Ui = np.zeros((len(results),t_max))
			Uj = np.zeros((len(results),t_max))
			Mi = np.zeros((len(results),t_max))
			Mj = np.zeros((len(results),t_max))
			
			for ii in range(len(results)):
				Si[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Si']
				Sj[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Sj']
				Ei[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Ei']
				Ej[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Ej']
				Ii[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Ii']
				Ij[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Ij']
				Ri[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Ri']
				Rj[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Rj']
				Hi[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Hi']
				Hj[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Hj']
				Ui[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Ui']
				Uj[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Uj']
				Mi[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Mi']
				Mj[ii,] = results[ii].query('omega_i == @omega_i & omega_j == @omega_j')['Mj']
		
        
		if IC_analysis == 3: # SENSITIVITY ANALYSIS
			plt.figure(i, figsize = tamfig)
			plt.style.use(fig_style)
			
			r0 = covid_parameters.beta / covid_parameters.gamma
			r0min = r0[0]
			r0max = r0[len(results) - 1]
         
			for ii in range(len(results)):
				a = (r0[ii] - r0min) / (r0max - r0min)
				plt.plot(t_space, Ii[ii, ] + Ij[ii, ],
						color = [a, 0, 1-a, 1],
                        label= f'$\omega_e={omega_i}$, $\omega_y={omega_j}$',
						linewidth = 0.5 )
		
			plt.title(main_title, fontsize=fsLabelTitle)
			plt.xlabel(main_label_x, fontsize=fsLabelTitle)
			plt.ylabel(main_label_y, fontsize=fsLabelTitle)
			mymap = mpl.colors.LinearSegmentedColormap.from_list(
                'mycolors',['blue','red'])
			sm = plt.cm.ScalarMappable(cmap=mymap, 
                                       norm=plt.Normalize(vmin=r0min, vmax=r0max))
			cbar = plt.colorbar(sm)
			cbar.set_label('Basic Reproduction Number', rotation = 90, fontsize=fsLabelTitle)
			
			plt.savefig(os.path.join(plot_dir,
								"I_" + filename + 'VariosR0' + filetype))
		else: # SINGLE RUN OR CONFIDENCE INTERVAL
				# INFECTADOS - DIFERENTES ISOLAMENTOS
			plt.figure(10, figsize = tamfig)
			plt.style.use(fig_style)
			
			if (IC_analysis == 1): # CONFIDENCE INTERVAL
				plt.plot(t_space,
						np.quantile(Ii+Ij, 0.5, axis=0), # MEDIANA
						ls[0],
						color = cor[2*i],
						label = f'$\omega_e={omega_i}$, $\omega_y={omega_j}$')
		
				plt.fill_between(t_space,
					np.quantile(Ii+Ij, 0.05, axis=0), # QUARTIL 5%
					np.quantile(Ii+Ij, 0.95, axis=0).clip(Ii[0,0]+Ij[0,0]), # QUARTIL 95%
					color=cor[2*i], alpha = 0.2)
			else: # SINGLE RUN
				plt.plot(t_space,
						(Ii+Ij),
						ls[0],
						color = cor[2*i],
						label = f'$\omega_e={omega_i}$, $\omega_y={omega_j}$')
				
			plt.title('Different isolation degrees', fontsize=fsLabelTitle)
			plt.legend(loc = leg_loc, fontsize=fsPlotLegend)
			plt.xlabel(main_label_x, fontsize=fsLabelTitle)
			plt.ylabel(main_label_y, fontsize=fsLabelTitle)		
			plt.savefig(os.path.join(plot_dir, "I_no_vert_horiz_isol" + filetype))
		
		
		
				# INFECTADOS - IDOSOS E JOVENS
			plt.figure(i, figsize = tamfig)
			plt.style.use(fig_style)
		
		
			if (IC_analysis == 1): # CONFIDENCE INTERVAL
				plt.plot(t_space,
					np.quantile(Ii, 0.5, axis=0),
					ls[0], color = cor[0])
				plt.plot(t_space,
					np.quantile(Ij, 0.5, axis=0),
					ls[1], color = cor[1])
		
				plt.fill_between(t_space,
					np.quantile(Ii, 0.05, axis = 0), 
					np.quantile(Ii, 0.95, axis = 0).clip(Ii[0,0]),
					color = cor[0], alpha=0.2)
				plt.fill_between(t_space,
					np.quantile(Ij, 0.05, axis = 0), 
					np.quantile(Ij, 0.95, axis = 0).clip(Ij[0,0]),
					color = cor[1], alpha=0.2)
			else: # SINGLE RUN
					plt.plot(t_space, Ii, ls[0], color = cor[0])
					plt.plot(t_space, Ij, ls[1], color = cor[1])
		
			plt.title(main_title, fontsize=fsLabelTitle)
			plt.legend(['Elderly', 'Young'],
				loc = leg_loc, fontsize=fsPlotLegend)
			plt.xlabel(main_label_x, fontsize=fsLabelTitle)
			plt.ylabel(main_label_y, fontsize=fsLabelTitle)
			
			plt.savefig(os.path.join(plot_dir, "Iey_" + filename  + filetype))
		
		
				# LEITOS DEMANDADOS - IDOSOS E JOVENS
			plt.figure(3+i, figsize = tamfig)
			plt.style.use(fig_style)
		
		
			if (IC_analysis == 1): # CONFIDENCE INTERVAL
				plt.plot(t_space, np.quantile(Hj, 0.5, axis=0), ls[1], color = cor[1])
				plt.plot(t_space, np.quantile(Hi, 0.5, axis=0), ls[0], color = cor[0])
				plt.plot(t_space, np.quantile(Ui, 0.5, axis=0), ls[0], color = cor[2])
				plt.plot(t_space, np.quantile(Uj, 0.5, axis=0), ls[1], color = cor[3])
		
				plt.fill_between(t_space,
					np.quantile(Hi, 0.05, axis=0), 
					np.quantile(Hi, 0.95, axis=0).clip(Hi[0,0]),
					color = cor[0], alpha=0.2)
				plt.fill_between(t_space,
					np.quantile(Hj, 0.05, axis=0), 
					np.quantile(Hj, 0.95, axis=0).clip(Hj[0,0]),
					color = cor[1], alpha=0.2)
				plt.fill_between(t_space,
					np.quantile(Ui, 0.05, axis=0), 
					np.quantile(Ui, 0.95, axis=0).clip(Ui[0,0]),
					color = cor[2], alpha=0.2)
				plt.fill_between(t_space,
					np.quantile(Uj, 0.05, axis=0), 
					np.quantile(Uj, 0.95, axis=0).clip(Uj[0,0]),
					color = cor[3], alpha=0.2)
			else: # SINGLE RUN
				plt.plot(t_space, Hi, ls[0], color = cor[0] )
				plt.plot(t_space, Hj, ls[1], color = cor[1] )
				plt.plot(t_space, Ui, ls[0], color = cor[2] )
				plt.plot(t_space, Uj, ls[1], color = cor[3] )
		
		
		
			plt.title(main_title, fontsize=fsLabelTitle)
			plt.legend(['Ward for Elderly', 'Ward for Young',
								'ICU for Elderly','ICU for Young'],
								loc = leg_loc, fontsize=fsPlotLegend)
			plt.xlabel(main_label_x, fontsize=fsLabelTitle)
			plt.ylabel('Bed Demand', fontsize=fsLabelTitle)		
			plt.savefig(os.path.join(plot_dir, "HUey_" + filename  + filetype))
		
		
				# OBITOS - IDOSOS E JOVENS
			plt.figure(6+i, figsize = tamfig)
			plt.style.use(fig_style)
		
		
			if (IC_analysis == 1): # CONFIDENCE INTERVAL
				plt.plot(t_space,
					np.quantile(Mi, 0.5, axis=0),
					ls[0], color = cor[0] )
				plt.plot(t_space,
					np.quantile(Mj, 0.5, axis=0),
					ls[1], color = cor[1] )
		
				plt.fill_between(t_space,
					np.quantile(Mi, 0.05, axis=0), 
					np.quantile(Mi, 0.95, axis=0).clip(Mi[0,0]),
					color = cor[0], alpha=0.2)
				plt.fill_between(t_space,
					np.quantile(Mj, 0.05, axis = 0), 
					np.quantile(Mj, 0.95, axis = 0).clip(Mj[0,0]),
					color = cor[1], alpha=0.2)
			else: # SINGLE RUN
				plt.plot(t_space, Mi, ls[0], color = cor[0])
				plt.plot(t_space, Mj, ls[1], color = cor[1])
		
			plt.title(main_title, fontsize=fsLabelTitle)
			plt.legend(['Elderly', 'Young'],
				loc = leg_loc, fontsize=fsPlotLegend)
			plt.xlabel(main_label_x, fontsize=fsLabelTitle)
			plt.ylabel('Deceased people', fontsize=fsLabelTitle)
			# ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
			plt.savefig(os.path.join(plot_dir, "Mey_" + filename  + filetype))
		
				

			
#		plt.figure(3+i)
#		plt.style.use('ggplot')

#		(results.query('omega_i == @omega_i & omega_j == @omega_j')
			# .div(1_000_000)
#			[['Hi', 'Hj', 'Ui', 'Uj']]
#			.plot(figsize=tamfig, fontsize=fsPlotLegend, logy=False)
#		)

#		plt.hlines(capacidade_leitos,
#					1, 
#					t_max, 
#					label=f'100% Leitos', colors='y', linestyles='dotted')

#		plt.hlines(capacidade_UTIs,
#					1, 
#					t_max, 
#					label=f'100% Leitos (UTI)', colors='y', linestyles='dashed')

#		plt.title(f'Demanda diaria de leitos: $N$={N}, ' + f'$\omega_i={omega_i}$, $\omega_j={omega_j}$', fontsize=fsLabelTitle)
#		plt.legend(['Leito normal idosos', 'Leito normal jovens', 'UTI idosos',
#				'UTI jovens', '100% Leitos', '100% UTIs'], fontsize=fsPlotLegend)
#		plt.xlabel('Dias', fontsize=fsLabelTitle)
#		plt.ylabel('Leitos', fontsize=fsLabelTitle)
#		plt.savefig(os.path.join(plot_dir, "HU_" + filename + ".png"))    
