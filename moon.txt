local targetPlaceId = 7449423635
local targetJobId = "05dc78b8-5172-4051-9413-f7ff059ff8d6"
local player = game:GetService("Players").LocalPlayer
local teleportService = game:GetService("TeleportService")
local isTeleporting = false

local function checkCurrentServer()
    if game.JobId == targetJobId then
        print("Already in the target server. Stopping script.")
        return true
    else
        print("Not in the target server. Preparing to teleport...")
        return false
    end
end

local function teleportToTargetServer()
    if not isTeleporting then
        isTeleporting = true
        local success, errorMessage = pcall(function()
            teleportService:TeleportToPlaceInstance(targetPlaceId, targetJobId, player)
        end)
        if not success then
            print("Teleport failed: " .. errorMessage)
            isTeleporting = false
        end
    end
end

local function startTeleportProcess()
    if not checkCurrentServer() then
        task.wait(2) -- รอ 2 วินาทีก่อนเทเลพอร์ต
        teleportToTargetServer()
    end
end

startTeleportProcess()
