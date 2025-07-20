# module "claude-code" {
#   source              = "registry.coder.com/coder/claude-code/coder"
#   version             = "2.0.2"
#   agent_id            = coder_agent.main.id
#   folder              = "/home/coder"
#   install_claude_code = true
#   claude_code_version = "latest"
# }

# module "jupyter-notebook" {
#   count    = data.coder_workspace.me.start_count
#   source   = "registry.coder.com/coder/jupyter-notebook/coder"
#   version  = "1.1.0"
#   agent_id = coder_agent.main.id
# }

module "jupyterlab" {
  count    = data.coder_workspace.me.start_count
  source   = "registry.coder.com/coder/jupyterlab/coder"
  version  = "1.1.0"
  agent_id = coder_agent.main.id
}