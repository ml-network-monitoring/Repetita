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
        List<Analysis> analysisList = new ArrayList();
        Topology topology = this.setting.getTopology();
        int nIterations = demandsList.size();

        // extract previous routing configuration
        RoutingConfiguration lastConfig = setting.getRoutingConfiguration();

        for (int iteration = 0; iteration < nIterations; iteration++) {
            // create new analysis
            // extract the new demand from demandsList
            Demands currentDemands = demandsList.get(iteration % demandsList.size());
            // create a new (minimalistic) setting and analyze it
            Setting currentSetting = new Setting();
            currentSetting.setTopology(topology);
            currentSetting.setDemands(currentDemands);
            currentSetting.setRoutingConfiguration(lastConfig);
            analysisList.add(analyzer.analyze(currentSetting));
            postOpt = analyzer.analyze(currentSetting);
            // TODO Set id
            this.analyses.put("iteration " + Integer.toString(iteration), analysisList.get(iteration));
            System.out.println("iteration " + Integer.toString(iteration), postOpt);
            // print results
            this.print(analyzer.compare(preOpt, analysisList.get(iteration)));
        }
        // END: Thanh-san code

        // save on paths file (if asked by the user)
        RepetitaWriter.writeToPathFile(FlowSimulator.getInstance().getNextHops());
    }
}
