-- calc_dissector.lua
-- Dissector for the CALC v1 protocol

local calc_proto = Proto("CALC", "CALC v1 Protocol")

-- Define protocol fields
local f_magic    = ProtoField.string("calc.magic", "Magic Bytes")
local f_version  = ProtoField.uint8("calc.version", "Version", base.DEC)
local f_msg_type = ProtoField.int32("calc.msg_type", "Message Type", base.DEC)
local f_text     = ProtoField.string("calc.text", "Text")
local f_op_code  = ProtoField.uint8("calc.op_code", "Operator Code", base.DEC)
local f_num1     = ProtoField.int32("calc.num1", "Number 1", base.DEC)
local f_num2     = ProtoField.int32("calc.num2", "Number 2", base.DEC)
local f_result   = ProtoField.int64("calc.result", "Result", base.DEC)

calc_proto.fields = {
  f_magic, f_version, f_msg_type, f_text, f_op_code, f_num1, f_num2, f_result
}

-- Constants for header size and expected values
local METADATA_SIZE = 5  -- 4 bytes magic + 1 byte version
local MAGIC = "CALC"
local VERSION = 1

function calc_proto.dissector(buffer, pinfo, tree)
  pinfo.cols.protocol = "CALC"
  
  local subtree = tree:add(calc_proto, buffer(), "CALC v1 Protocol Data")
  
  if buffer:len() < METADATA_SIZE then return end

  -- Parse metadata header
  local magic = buffer(0, 4):string()
  local version = buffer(4, 1):uint()
  
  subtree:add(f_magic, buffer(0,4))
  subtree:add(f_version, buffer(4,1))
  
  if magic ~= MAGIC or version ~= VERSION then
    subtree:add_expert_info(PI_PROTOCOL, PI_ERROR, "Invalid CALC header")
    return
  end
  
  -- The remaining payload begins after the 5-byte header.
  local payload = buffer(METADATA_SIZE)
  local payload_len = payload:len()
  
  -- Determine message type based on payload length.
  if payload_len == 20 then
    -- Likely a heartbeat message: 4-byte msg_type and 16-byte text.
    subtree:add(f_msg_type, payload(0,4))
    subtree:add(f_text, payload(4,16))
    pinfo.cols.info = "CALC Heartbeat"
  
  elseif payload_len == 13 then
    -- Operation Request: 4-byte msg_type, 1-byte op_code, 4-byte num1, 4-byte num2.
    subtree:add(f_msg_type, payload(0,4))
    subtree:add(f_op_code, payload(4,1))
    subtree:add(f_num1, payload(5,4))
    subtree:add(f_num2, payload(9,4))
    pinfo.cols.info = "CALC Operation Request"
  
  elseif payload_len == 12 then
    -- Operation Response: 4-byte msg_type, 8-byte result.
    subtree:add(f_msg_type, payload(0,4))
    subtree:add(f_result, payload(4,8))
    pinfo.cols.info = "CALC Operation Response"
  
  else
    subtree:add_expert_info(PI_PROTOCOL, PI_ERROR, "Unknown payload length")
  end
end

-- Register the dissector for a specific TCP port (for example, 6000)
local tcp_port = DissectorTable.get("tcp.port")
tcp_port:add(6000, calc_proto)
