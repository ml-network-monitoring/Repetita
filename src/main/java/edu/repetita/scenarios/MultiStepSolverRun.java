package edu.repetita.scenarios;

import edu.repetita.core.*;
import edu.repetita.analyses.Analysis;
import edu.repetita.io.RepetitaWriter;
import edu.repetita.simulators.FlowSimulator;
import edu.repetita.analyses.Analyzer;


import java.util.List;


/*
 *  Basic scenario: we run the solvers for a set amount of time,
 *  and check the maximum link utilization of the returned paths.
 */

public class MultiStepSolverRun extends Scenario {
    private Analyzer analyzer = Analyzer.getInstance();

    @Override
    public String getDescription() {
        return "Runs the given solver on an input setting";
    }

    @Override
    public void run(long timeMillis) {
        // perform pre-optimization analyses
        Analysis preOpt = analyzer.analyze(this.setting);
        preOpt.setId("pre-optimization");
        if (this.keepAnalyses){
            this.analyses.put("pre-optimization",preOpt);
        }

        // ask the solver to optimize
        this.solver.solve(this.setting,timeMillis);
        long optTime = this.solver.solveTime(this.setting);


        // perform post-optimization analyses
        Analysis postOpt = analyzer.analyze(this.setting);
        postOpt.setId("post-optimization");
        if (this.keepAnalyses){
            this.analyses.put("post-optimization", postOpt);
        }

        // print results
        this.print(analyzer.compare(preOpt, postOpt));
        this.print("Optimization time (in seconds): " + optTime / 1000000000.0);

        // BEGIN: Thanh-san code
        // extract useful information from setting like topo and demandchanges
        List<Demands> demandsList = this.setting.getDemandChanges();
        Topology topology = this.setting.getTopology();
        int nIterations = demandsList.size();

        System.out.println("nIterations: " + nIterations);

        // extract previous routing configuration
        RoutingConfiguration lastConfig = setting.getRoutingConfiguration();

        // initialize a setting
        Setting currentSetting = new Setting();
        currentSetting.setTopology(topology);
        currentSetting.setRoutingConfiguration(lastConfig);
        Demands currentDemands;
        for (int iteration = 0; iteration < nIterations; iteration++) {
            // extract the new demand from demandsList
            currentDemands = demandsList.get(iteration);
            System.out.println(currentDemands.amount);
            // create a new (minimalistic) setting and analyze it
            currentSetting.setDemands(currentDemands);
            System.out.println("before analyses");
            this.analyses.put("Iteration " + Integer.toString(iteration), analyzer.analyze(currentSetting));
            System.out.println("after analyses");
        }

        // print results
        for (int it = 0; it < nIterations; it++) {
            this.print("\ndemand change " + it);
            this.analyses.get("Iteration " + Integer.toString(it)).printTrafficSummary();
        }
        // END: Thanh-san code

        // save on paths file (if asked by the user)
        RepetitaWriter.writeToPathFile(FlowSimulator.getInstance().getNextHops());
    }
}
