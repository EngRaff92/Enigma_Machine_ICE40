//! APB_MODULE: Slave Type
//! Simple APB module that behaves as SLAVE. The internal FSM is made by 2 Main Processes
//! First one:  State changing on Clock (Back to IDLE in case of RESET). The reset condition
//!             could be either SYNC or ASYNC with the main clock
//! Second one: State transition and evaluation
//! One quick note on thhe Slave Error signal usually is an output. But the Slave has no concept of 
//! error since there is no error condition in it simply drives signals hence the slaverror is tied 
//! to an input driven by the module where this module is instatiated

/** Time Scale */
`timescale 1ns/1ns

/** MODULE */
module apb_slave_wrapper #(
    // Parameters
    parameter DATA_WIDTH    = 32,  //! 
    parameter ADDR_WIDTH    = 5,   //!
    parameter [800:0] IMAGE = ""   //! 
) (
    // Input ports
    input logic                     clock,      //!
    input logic                     ares,       //!
    input logic                     psel,       //!
    input logic                     pwrite,     //!
    input logic                     penable,    //!
    input logic [ADDR_WIDTH-1:0]    paddr,      //!
    input logic [DATA_WIDTH-1:0]    pwdata,     //!
    input logic                     prot,       //!
    input logic                     pstrb,      //!
    // Output ports
    output logic [DATA_WIDTH-1:0]   prdata,     //!
    output logic                    pslverror,  //!
    output logic                    pready      //!
);
    
    /** Local Parameters */
    localparam WAIT_SATES   = 0;    
    localparam SYNC_PROC    = 0;    
    localparam TIEOFF_ERR   = 0;
    localparam ATW          = 5;    
    localparam DEPTH        = 32;   
    localparam DATAW        = 32;   
    localparam ZEROR        = 0;
    localparam ISCLK        = 0;     

    /** internal Signals mainly as memory interface */
    logic                   m_write;
    logic                   m_cs;
    logic [ADDR_WIDTH-1:0]  m_addr;
    logic [DATA_WIDTH-1:0]  m_wdata;
    logic                   m_prot;
    logic [DATA_WIDTH-1:0]  m_rdata;
    logic                   m_error;

    /** ROM */
    rom#(
        .ATW    (ATW),
        .DEPTH  (DEPTH),
        .DATAW  (DATAW),
        .ZEROR  (ZEROR),
        .IMAGE  (IMAGE),
        .ISCLK  (ISCLK)
    ) u_rom (
        // INPUT
        .mem_clk    (clock),
        .mem_cs     (m_cs),
        .mem_address(m_addr),
        .mem_op     (m_write),
        .mem_wdata  (m_wdata),
        // OUTPUT
        .mem_rdata  (m_rdata)
    );

    /** APB SLAVE */
    apb_slave#() u_apb_slave(
        // STD PORT
        // INPUT
        .apb_clock      (clock),
        .apb_ares       (ares),
        .apb_addr       (paddr),
        .apb_penable    (penable),
        .apb_prot       (prot),
        .apb_wdata      (pwdata),
        .apb_psel       (psel),
        .apb_pwrite     (pwrite),
        .apb_strb       (pstrb),
        // OUTPUT
        .apb_pready     (pready),        
        .apb_rdata      (prdata),
        .apb_slverror   (pslverror),
        // PORT FORWARDING
        // INPUT
        .fslverror      (1'b0),
        .frdata         (m_rdata),
        // OUTPUT
        .fwrite         (m_write),  
        .fenable        (m_cs),
        .fwdata         (m_wdata),      
        .fprot          (m_prot),                
        .faddr          (m_addr)
    );

    /** WAVES */
    integer j;
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0);
        for(j=0; j<DEPTH; j++) $dumpvars(1, u_rom.MEMARRAY[j]);     
    end
endmodule // apb_slave_wrapper