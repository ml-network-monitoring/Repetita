package edu.repetita.analyses.specialized;

import edu.repetita.core.Setting;
import edu.repetita.analyses.Analysis;
import edu.repetita.simulators.FlowSimulator;
import edu.repetita.utils.MCF;

import java.util.ArrayList;
import java.util.List;

public class FlowSpecializedAnalyzer implements SpecializedAnalyzer {
    private FlowSimulator flowSimulator = FlowSimulator.getInstance();
    private boolean compareWithMCF = false;

    public void setCompareWithMCF(){
        this.compareWithMCF = true;
    }

    @Override
    public List<String> getDescription() {
        return new ArrayList(){{
            add("maximum link utilization, optionally including comparison with the theoretical lower bound (MCF solution)");
        }};
    }

    @Override
    public void analyze(Setting setting, Analysis analysis) {
        System.out.println("pass");
        flowSimulator.setup(setting);
        System.out.println("pass");
        flowSimulator.computeFlows();

        System.out.println("pass");
        analysis.maxLinkLoad = this.getMaxLoad();
        double mcfLoad = -1;
        System.out.println("pass");
        if (this.compareWithMCF){
            MCF mcfComputer = new MCF(setting.getTopology(), setting.getDemands(), false);
            mcfLoad = mcfComputer.computeMaxUtilization();
        }
        System.out.println("pass");
        analysis.maxLinkLoadLowerBound = mcfLoad;
    }

    @Override
    public String compare(Analysis firstAnalysis, Analysis secondAnalysis, String firstTag, String secondTag){
        StringBuilder sb = new StringBuilder();

        // compare maxLinkLoad
        sb.append(firstTag).append(" max link utilization ").append(firstAnalysis.maxLinkLoad).append("\n");
        sb.append(secondTag).append(" max link utilization ").append(secondAnalysis.maxLinkLoad).append("\n");

        // future additional comparison to be added here...

        return sb.toString();
    }

    /* Analyses on objective function(s) */

    private double getMaxLoad(){
        return flowSimulator.getMaxUtilization();
    }
}
