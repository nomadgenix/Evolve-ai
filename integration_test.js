// Integration test script for Evolve frontend-backend communication

// This file should be run in the browser console after starting both 
// the frontend and backend services to validate proper communication

// Test authentication
async function testAuthentication() {
  console.log("Testing authentication...");
  
  try {
    // Test registration
    console.log("Testing registration...");
    const registerData = {
      username: "testuser_" + Math.floor(Math.random() * 10000),
      email: `test${Math.floor(Math.random() * 10000)}@evolve.ai`,
      password: "testpassword123"
    };
    
    const registerResult = await window.evolveApi.register(registerData);
    console.log("Registration result:", registerResult);
    
    // Test login
    console.log("Testing login...");
    const loginResult = await window.evolveApi.login(registerData.username, registerData.password);
    console.log("Login result:", loginResult);
    
    return true;
  } catch (error) {
    console.error("Authentication test failed:", error);
    return false;
  }
}

// Test agent management
async function testAgentManagement() {
  console.log("Testing agent management...");
  
  try {
    // Create agent
    console.log("Creating test agent...");
    const agentData = {
      name: "Test Agent " + Math.floor(Math.random() * 10000),
      description: "Test agent for integration testing",
      model: "gpt-3.5-turbo"
    };
    
    const createdAgent = await window.evolveApi.createAgent(agentData);
    console.log("Created agent:", createdAgent);
    
    // Get agent
    console.log("Fetching agent...");
    const fetchedAgent = await window.evolveApi.getAgent(createdAgent.id);
    console.log("Fetched agent:", fetchedAgent);
    
    // Update agent
    console.log("Updating agent...");
    const updatedData = {
      ...agentData,
      description: "Updated description for testing"
    };
    
    const updatedAgent = await window.evolveApi.updateAgent(createdAgent.id, updatedData);
    console.log("Updated agent:", updatedAgent);
    
    // List agents
    console.log("Listing all agents...");
    const agents = await window.evolveApi.fetchAgents();
    console.log("All agents:", agents);
    
    return true;
  } catch (error) {
    console.error("Agent management test failed:", error);
    return false;
  }
}

// Test agent execution
async function testAgentExecution() {
  console.log("Testing agent execution...");
  
  try {
    // Get first agent
    const agents = await window.evolveApi.fetchAgents();
    if (agents.length === 0) {
      console.error("No agents available for testing execution");
      return false;
    }
    
    const agentId = agents[0].id;
    
    // Run agent
    console.log(`Running agent ${agentId}...`);
    const execution = await window.evolveApi.runAgent(agentId, "Hello, this is a test input");
    console.log("Execution started:", execution);
    
    // Wait for execution to complete
    console.log("Waiting for execution to complete...");
    let executionResult;
    let attempts = 0;
    
    while (attempts < 10) {
      executionResult = await window.evolveApi.getExecution(execution.id);
      console.log("Execution status:", executionResult.status);
      
      if (executionResult.status === "completed" || executionResult.status === "failed") {
        break;
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      attempts++;
    }
    
    console.log("Final execution result:", executionResult);
    
    return true;
  } catch (error) {
    console.error("Agent execution test failed:", error);
    return false;
  }
}

// Test tools management
async function testToolsManagement() {
  console.log("Testing tools management...");
  
  try {
    // List tools
    console.log("Listing all tools...");
    const tools = await window.evolveApi.fetchTools();
    console.log("All tools:", tools);
    
    if (tools.length === 0) {
      console.warn("No tools available for testing");
      return true;
    }
    
    // Get first agent
    const agents = await window.evolveApi.fetchAgents();
    if (agents.length === 0) {
      console.error("No agents available for testing tools");
      return false;
    }
    
    const agentId = agents[0].id;
    const toolId = tools[0].id;
    
    // Add tool to agent
    console.log(`Adding tool ${toolId} to agent ${agentId}...`);
    const addResult = await window.evolveApi.addToolToAgent(agentId, toolId, '{"param": "value"}');
    console.log("Tool added:", addResult);
    
    // Remove tool from agent
    console.log(`Removing tool ${toolId} from agent ${agentId}...`);
    const removeResult = await window.evolveApi.removeToolFromAgent(agentId, toolId);
    console.log("Tool removed:", removeResult);
    
    return true;
  } catch (error) {
    console.error("Tools management test failed:", error);
    return false;
  }
}

// Run all tests
async function runIntegrationTests() {
  console.log("Starting Evolve integration tests...");
  
  // Make API available globally for testing
  window.evolveApi = window.api;
  
  const authResult = await testAuthentication();
  const agentResult = await testAgentManagement();
  const executionResult = await testAgentExecution();
  const toolsResult = await testToolsManagement();
  
  console.log("Integration test results:");
  console.log("- Authentication:", authResult ? "PASSED" : "FAILED");
  console.log("- Agent Management:", agentResult ? "PASSED" : "FAILED");
  console.log("- Agent Execution:", executionResult ? "PASSED" : "FAILED");
  console.log("- Tools Management:", toolsResult ? "PASSED" : "FAILED");
  
  const allPassed = authResult && agentResult && executionResult && toolsResult;
  console.log("Overall result:", allPassed ? "PASSED" : "FAILED");
  
  return allPassed;
}

// Export for browser use
if (typeof window !== 'undefined') {
  window.runEvolveTests = runIntegrationTests;
  console.log("Integration tests ready. Run window.runEvolveTests() to start testing.");
}
