-- สร้าง UI
local ScreenGui = Instance.new("ScreenGui")
local PlayerCountLabel = Instance.new("TextLabel")
local FPSLabel = Instance.new("TextLabel")
local UsernameLabel = Instance.new("TextLabel")
local MoonLabel = Instance.new("TextLabel")
local TimeLabel = Instance.new("TextLabel")

-- ลบ UI เดิมก่อนสร้างใหม่ (ป้องกันการซ้อนทับ)
local playerGui = game.Players.LocalPlayer:WaitForChild("PlayerGui")
if playerGui:FindFirstChild("PlayerInfoUI") then
    playerGui:FindFirstChild("PlayerInfoUI"):Destroy()
end

-- ตั้งค่า ScreenGui
ScreenGui.Name = "PlayerInfoUI"
ScreenGui.Parent = playerGui
ScreenGui.ResetOnSpawn = false

-- ตั้งค่า PlayerCountLabel
PlayerCountLabel.Name = "PlayerCountLabel"
PlayerCountLabel.Parent = ScreenGui
PlayerCountLabel.BackgroundTransparency = 1
PlayerCountLabel.Position = UDim2.new(0.01, 0, 0.01, 0)
PlayerCountLabel.Size = UDim2.new(0.2, 0, 0.05, 0)
PlayerCountLabel.Font = Enum.Font.GothamBold
PlayerCountLabel.Text = "0 Players"
PlayerCountLabel.TextColor3 = Color3.new(1, 1, 1)
PlayerCountLabel.TextScaled = true
PlayerCountLabel.TextXAlignment = Enum.TextXAlignment.Left
PlayerCountLabel.TextStrokeTransparency = 0
PlayerCountLabel.TextStrokeColor3 = Color3.new(0, 0, 0)

-- ตั้งค่า FPSLabel
FPSLabel.Name = "FPSLabel"
FPSLabel.Parent = ScreenGui
FPSLabel.BackgroundTransparency = 1
FPSLabel.Position = UDim2.new(0.01, 0, 0.07, 0)
FPSLabel.Size = UDim2.new(0.2, 0, 0.05, 0)
FPSLabel.Font = Enum.Font.GothamBold
FPSLabel.Text = "FPS: 0"
FPSLabel.TextColor3 = Color3.new(1, 1, 1)
FPSLabel.TextScaled = true
FPSLabel.TextXAlignment = Enum.TextXAlignment.Left
FPSLabel.TextStrokeTransparency = 0
FPSLabel.TextStrokeColor3 = Color3.new(0, 0, 0)

-- ตั้งค่า UsernameLabel
UsernameLabel.Name = "UsernameLabel"
UsernameLabel.Parent = ScreenGui
UsernameLabel.BackgroundTransparency = 1
UsernameLabel.Position = UDim2.new(0.01, 0, 0.13, 0)
UsernameLabel.Size = UDim2.new(0.2, 0, 0.05, 0)
UsernameLabel.Font = Enum.Font.GothamBold
UsernameLabel.Text = "User: " .. game.Players.LocalPlayer.DisplayName
UsernameLabel.TextColor3 = Color3.new(1, 1, 1)
UsernameLabel.TextScaled = true
UsernameLabel.TextXAlignment = Enum.TextXAlignment.Left
UsernameLabel.TextStrokeTransparency = 0
UsernameLabel.TextStrokeColor3 = Color3.new(0, 0, 0)

-- ตั้งค่า MoonLabel
MoonLabel.Name = "MoonLabel"
MoonLabel.Parent = ScreenGui
MoonLabel.BackgroundTransparency = 1
MoonLabel.Position = UDim2.new(0.01, 0, 0.19, 0)
MoonLabel.Size = UDim2.new(0.2, 0, 0.05, 0)
MoonLabel.Font = Enum.Font.GothamBold
MoonLabel.Text = "Moon: 🌑"
MoonLabel.TextColor3 = Color3.new(1, 1, 1)
MoonLabel.TextScaled = true
MoonLabel.TextXAlignment = Enum.TextXAlignment.Left
MoonLabel.TextStrokeTransparency = 0
MoonLabel.TextStrokeColor3 = Color3.new(0, 0, 0)

-- ตั้งค่า TimeLabel
TimeLabel.Name = "TimeLabel"
TimeLabel.Parent = ScreenGui
TimeLabel.BackgroundTransparency = 1
TimeLabel.Position = UDim2.new(0.01, 0, 0.25, 0)
TimeLabel.Size = UDim2.new(0.2, 0, 0.05, 0)
TimeLabel.Font = Enum.Font.GothamBold
TimeLabel.Text = "Time: 00:00"
TimeLabel.TextColor3 = Color3.new(1, 1, 1)
TimeLabel.TextScaled = true
TimeLabel.TextXAlignment = Enum.TextXAlignment.Left
TimeLabel.TextStrokeTransparency = 0
TimeLabel.TextStrokeColor3 = Color3.new(0, 0, 0)

-- ฟังก์ชันสำหรับอัปเดตจำนวนผู้เล่น
local function updatePlayerCount()
    local players = game.Players:GetPlayers()
    PlayerCountLabel.Text = #players .. " Players"
end

-- อัปเดตจำนวนผู้เล่นเมื่อมีการเปลี่ยนแปลง
game.Players.PlayerAdded:Connect(updatePlayerCount)
game.Players.PlayerRemoving:Connect(updatePlayerCount)

-- อัปเดตจำนวนผู้เล่นครั้งแรก
updatePlayerCount()

-- ฟังก์ชันสำหรับอัปเดต FPS
local RunService = game:GetService("RunService")
local lastTime = tick()
local frameCount = 0

RunService.RenderStepped:Connect(function()
    frameCount = frameCount + 1
    local currentTime = tick()
    if currentTime - lastTime >= 1 then
        FPSLabel.Text = "FPS: " .. frameCount
        frameCount = 0
        lastTime = currentTime
    end
end)

-- ฟังก์ชันสำหรับอัปเดต Moon และเวลา
local function updateMoonAndTime()
    local Moon = {
        ['8'] = "http://www.roblox.com/asset/?id=9709149431", -- 🌕
        ['7'] = "http://www.roblox.com/asset/?id=9709149052", -- 🌖
        ['6'] = "http://www.roblox.com/asset/?id=9709143733", -- 🌗
        ['5'] = "http://www.roblox.com/asset/?id=9709150401", -- 🌘
        ['4'] = "http://www.roblox.com/asset/?id=9709135895", -- 🌑
        ['3'] = "http://www.roblox.com/asset/?id=9709139597", -- 🌒
        ['2'] = "http://www.roblox.com/asset/?id=9709150086", -- 🌓
        ['1'] = "http://www.roblox.com/asset/?id=9709149680", -- 🌔
    }

    local MoonTextureId = game:GetService("Lighting").Sky.MoonTextureId
    local MoonIcon

    if MoonTextureId == Moon['1'] then
        MoonIcon = '🌕'
    elseif MoonTextureId == Moon['2'] then
        MoonIcon = '🌓'
    elseif MoonTextureId == Moon['3'] then
        MoonIcon = '🌒'
    elseif MoonTextureId == Moon['4'] then
        MoonIcon = '🌑'
    elseif MoonTextureId == Moon['5'] then
        MoonIcon = '🌘'
    elseif MoonTextureId == Moon['6'] then
        MoonIcon = '🌗'
    elseif MoonTextureId == Moon['7'] then
        MoonIcon = '🌖'
    elseif MoonTextureId == Moon['8'] then
        MoonIcon = '🌕'
    end

    MoonLabel.Text = "Moon: " .. MoonIcon
    TimeLabel.Text = "Time: " .. game.Lighting.TimeOfDay
end

-- เรียกใช้ครั้งแรก
updateMoonAndTime()

-- อัปเดตเมื่อ Sky เปลี่ยนแปลง
game:GetService("Lighting").Sky:GetPropertyChangedSignal("MoonTextureId"):Connect(updateMoonAndTime)
RunService.Heartbeat:Connect(updateMoonAndTime)
