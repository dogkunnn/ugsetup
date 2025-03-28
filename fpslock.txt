local RunService = game:GetService("RunService")

local TARGET_FRAME_RATE = 30

local frameStart = os.clock()

RunService.PreSimulation:Connect(function()
	while os.clock() - frameStart < 1 / TARGET_FRAME_RATE do
		-- We do nothing until the target time has elapsed
	end

	-- Mark the start of the next frame right before this one is rendered
	frameStart = os.clock()
end)
